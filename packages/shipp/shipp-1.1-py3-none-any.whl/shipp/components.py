'''
Module components
Contains classes to describe the components of an hybrid power plant

Class Storage:
    Represent storage system that can be charged or discharged

Class Production:
    Represent a power plant (wind or pv) production electricity from
    a given resource
'''

import matplotlib.pyplot as plt
import numpy as np
import numpy_financial as npf

from shipp.timeseries import TimeSeries

class Storage:
    '''
    Class Storage used to represent energy storage systems

    Attributes:
        e_cap (float): Energy capacity [MWh]
        p_cap (float): Power capacity [MW]
        eff_in (float): Efficiency to charge the storage [-]
        eff_out (float): Efficiency to discharge the storage [-]
        e_cost (float): Cost per unit of energy capacity [Currency/MWh]
        p_cost (float): Cost per unit of power capacity [Currency/MW]
    '''

    def __init__(self, e_cap: float = 0, p_cap: float = 0,
                 eff_in: float = 1, eff_out: float = 1, e_cost: float = 0,
                 p_cost: float = 0) -> None:
        self.e_cap = e_cap
        self.p_cap = p_cap
        self.eff_in = eff_in
        self.eff_out = eff_out
        self.e_cost = e_cost
        self.p_cost = p_cost

    def get_av_eff(self) -> float:
        '''Returns the average efficiency'''
        return 0.5*(self.eff_in + self.eff_out)

    def get_rt_eff(self) -> float:
        '''Returns the round trip efficiency'''
        return self.eff_in*self.eff_out

    def get_tot_costs(self) -> float:
        '''Returns total costs for the storage'''
        return self.p_cap * self.p_cost + self.e_cap * self.e_cost
    
    def __repr__(self) -> str:
        return (f"Storage(e_cap={self.e_cap}, p_cap={self.p_cap}, eff_in={self.eff_in}, "
                f"eff_out={self.eff_out}, e_cost={self.e_cost}, p_cost={self.p_cost})")


class Production:
    '''
    Class Production represents wind or solar PV production systems

    Attributes:
        power_ts (TimeSeries): time series of power production [MW]
        p_max (float): Maximum power [MW]
        p_cost (float): cost per unit of power capacity [Currency/MW]
    '''
    def __init__(self, power_ts: TimeSeries, p_cost: float = 0) -> None:
        self.power = power_ts
        self.p_max = max(self.power.data)
        self.p_cost = p_cost

    def get_tot_costs(self) -> float:
        '''Returns total costs for the production'''
        return self.p_max * self.p_cost
    
    def __repr__(self) -> str:
        return (f"Production(p_cost={self.p_cost}, p_max={self.p_max}, "
                f"power={self.power})")

class OpSchedule:
    '''
    Class OpSchedule describes a realization of an energy schedule
    and renewable electric production units.

    Attributes:
        storage_list (list[Storage]): List of energy storage units.
        production_list (list[Production]): List of renewable power production units.
        production_p (list[TimeSeries]): List of TimeSeries for the power output of production units.
        storage_p (list[TimeSeries]): List of TimeSeries for the power output of storage units.
        storage_e (list[TimeSeries]): List of TimeSeries for the energy level of storage objects.
        power_out (TimeSeries): TimeSeries of total power to the grid.
        revenue (float): Total annual revenue from selling electricity.
        capex (float): Total capital expenditure from storage and production objects.
        revenue_storage (float): Total annual revenue from storage units.
        npv (float): Net Present Value of the operation schedule.
        irr (float): Internal Rate of Return of the operation schedule.
        a_npv (float): Added Net Present Value due to the addition of storage.
    '''

    def __init__(self,
                 production_list: list[Production],
                 storage_list: list[Storage],
                 production_p: list[TimeSeries],
                 storage_p: list[TimeSeries],
                 storage_e: list[TimeSeries],
                 price: list[float] = None) -> None:
        '''
        Initialization function for OpSchedule
        '''
        self.production_list = production_list
        self.storage_list = storage_list
        self.production_p = production_p
        self.storage_p = storage_p
        self.storage_e = storage_e

        # Calculation of the power to the grid (power_out)
        power_out_data = np.zeros_like(production_p[0].data)
        power_out_dt = self.production_p[0].dt

        for item in self.production_p:
            assert power_out_dt == item.dt
            power_out_data += item.data

        for item in self.storage_p:
            assert power_out_dt == item.dt
            power_out_data += item.data

        self.power_out = TimeSeries(power_out_data, power_out_dt)

        # Calculation of the revenue is the price is provided
        self.revenue = None
        if price is not None:
            self.update_revenue(price)

        # Calculation of CAPEX 
        self.update_capex()

    def update_capex(self) -> None:
        '''
        Function to calculate the total CAPEX from Storage and 
        Production objects
        '''
        self.capex = 0
        for item in self.production_list:
            self.capex += item.get_tot_costs()
        for item in self.storage_list:
            self.capex += item.get_tot_costs()


    def update_revenue(self, price: list[float]) -> None:
        '''
        Function to calculate the yearly revenue for the operating 
        schedule. The revenue is obtained by selling the electricity 
        to the grid (power_out) at the given price
        
        Params:
            price [currency/MWh]: day-ahead market price 
        '''
        n = min(len(price), len(self.power_out.data))
        dot_product = np.dot(price[:n], self.power_out.data[:n])

        self.revenue = 365*24/n * dot_product*self.power_out.dt

        self.revenue_storage = 0
        for power in self.storage_p:
            dot_product = np.dot(price[:n], power.data[:n])
            self.revenue_storage += 365*24/n * dot_product * power.dt


    def get_npv_irr(self, discount_rate: float,
                    n_year: int) -> tuple[float, float]:
        '''
        Function to calculate the Net Present Value (npv) and 
        internal rate of return (irr) for the OpSchedule object
        Params:
            discount rate [-]: Usually 3, 7 or 10% for wind energy
                project
            n_year [-]: Number of years of operation
        Returns:
            npv [M.currency]: Net Present Value
            irr [-]: Internal Rate of return
        '''
        assert self.revenue is not None
        assert 0 <= discount_rate <=1
        assert isinstance(n_year, int)

        cash_flow = [-self.capex]

        for _ in range(1,n_year):
            cash_flow.append(self.revenue)

        npv = npf.npv(discount_rate, cash_flow) * 1e-6
        irr = npf.irr(cash_flow)

        self.npv = npv
        self.irr = irr

        return npv, irr
    
    def get_added_npv(self, discount_rate: float,
                    n_year: int) -> tuple[float, float]:
        '''
        Function to calculate the difference in Net Present Value 
        due to the addition of the storage

        Params:
            discount rate [-]: Usually 3, 7 or 10% for wind energy
                project
            n_year [-]: Number of years of operation

        Returns:
            a_npv [M.currency] added Net Present Value
        '''
        assert self.revenue_storage is not None
        assert 0 <= discount_rate <=1
        assert isinstance(n_year, int)

        capex_storage = 0
        for item in self.storage_list:
            capex_storage += item.get_tot_costs()

        cash_flow = [-capex_storage]

        for _ in range(1,n_year):
            cash_flow.append(self.revenue_storage)

        a_npv = npf.npv(discount_rate, cash_flow) * 1e-6

        self.a_npv = a_npv

        return a_npv

    def get_power_partition(self) -> list[float]:
        '''
        Function to calculate the partition of the total power 
        production for each component, expressed as percentage of 
        the total energy produced.
        
        Returns:
            percent [-] array of percentage corresponding to the 
            objects in self.production_list and then the one in 
            self.storage_list
        '''
        dt = self.production_p[0].dt

        total_energy = dt * sum(self.power_out.data)

        percent = []

        # Calculation of the portion of energy used to charge (power<0) 
        # the storage 
        percent_charge_storage = 0
        for power in self.storage_p:
            percent_charge_storage += sum(np.minimum(power.data, 0))*dt \
                /total_energy

        # Calculation of the portion of energy produced by the 
        # production item
        for power in self.production_p:
            percent.append((sum(power.data)*dt) / total_energy)

        # Calculation of the portion of energy discharged (power>=0) 
        # from the storage 
        for power in self.storage_p:
            percent.append(sum(np.maximum(0,power.data))*dt / total_energy)

        # The energy used for storage charge (power<0) is removed from 
        # the energy produced by production units. Here, we use the 
        # first production unit
        percent[0] += percent_charge_storage

        return percent

    def check_losses(self, tol: float, verbose: bool = False) -> bool:
        '''
        Check the losses in the model and verify if they are within the tolerance.
        Params:
            tol: The tolerance level for the losses.
            verbose: If True, prints the error values. Default is False.
            
        Returns:
            bool: True if the losses are within the tolerance, False otherwise.
        '''
        verifiedModel = True

        if hasattr(self, 'losses'):
            for los, pow, stor in zip(self.losses, self.storage_p, 
                                      self.storage_list):
                wdw_in = np.where(pow.data < 0)
                wdw_out = np.where(pow.data >=0)

                diff_in = los[wdw_in] + (1-stor.eff_in)* pow.data[wdw_in]
                diff_out = los[wdw_out] - (1-stor.eff_out)/stor.eff_out* \
                                            pow.data[wdw_out]

                error_in = sum( eps**2 for eps in diff_in)
                error_out = sum( eps**2 for eps in diff_out)
                if verbose:
                    print('Error : {:.2e}\t{:.2e}'.format(error_in, error_out))
                if error_in > tol or error_out > tol:
                    verifiedModel = False
        else:
            print('Warning: check_losses(): OpSchedule object does not have losses')

        return verifiedModel

    def plot_powerflow(self, label_list: list[str] = None,
                       xlabel: str = 'Time [day]',
                       ylabel1: str = 'Power [MW]',
                       ylabel2: str = 'Energy [MWh]') -> None:
        '''
        Function to plot the power flow of the operation schedule

        Params:
            label_list: list of labels to appear on the legend
            xlabel: label of the x-axis
            ylabel1: label of the y-axis (left) for power
            ylabel2: label of the y-axis (right) for energy
        '''
        if label_list is None:
            label_list = []
            cnt = 0
            for storage_item in self.storage_p:
                label_list.append('Storage P ' + str(cnt))
                cnt+=1
            cnt = 0
            for production_item in self.production_p:
                label_list.append('Production P' + str(cnt))
                cnt+=1
            cnt = 0
            for storage_item in self.storage_e:
                label_list.append('Storage E ' + str(cnt))
                cnt+=1

        cnt = 0

        for storage_item in self.storage_p:
            if storage_item.data is not None:
                plt.plot(storage_item.time() * 1/24, storage_item.data,
                         color = 'none') #label = label_list[cnt]
                cnt+=1

        for production_item in self.production_p:
            if production_item.data is not None:
                plt.plot(production_item.time() * 1/24, production_item.data,
                         label = label_list[cnt])
                cnt+=1

        plt.ylabel(ylabel1)
        plt.xlabel(xlabel)
        plt.twinx()

        for storage_item in self.storage_e:
            if storage_item.data is not None:
                plt.plot(storage_item.time()* 1/24, storage_item.data, '--',
                         label = label_list[cnt])
                cnt+=1

        plt.ylabel(ylabel2)

        # Manually specify the labels and lines for the legend
        lines = []
        labels = []

        for ax in plt.gcf().get_axes():
            for line in ax.get_lines():
                lines.append(line)
                labels.append(line.get_label())

        # Create a single legend that includes both sets of labels
        plt.legend(lines, labels)

    def plot_powerout(self, label_list: list[str] = None,
                      xlabel: str = 'Time [day]',
                      ylabel: str = 'Power [MW]',
                      xlim: list[float] = None) -> None:
        '''
        Function to plot the power the operation schedule, focusing
        on the power sent to the grid (power "out").

        Params:
            label_list: list of labels to appear on the legend
            xlabel: label of the x-axis
            ylabel: label of the y-axis for power
            xlim [2,]: x range limits for the plot, allows to
            reduce computational effort
        '''
        if label_list is None:
            cnt = 0
            label_list = []
            for storage_item in self.storage_p:
                label_list.append('Storage P ' + str(cnt))
                cnt+=1
            cnt = 0
            for production_item in self.production_p:
                label_list.append('Production P' + str(cnt))
                cnt+=1

        dt_all = self.storage_p[0].dt

        if xlim is None or len(xlim) != 2:
            xlim = [0, len(self.power_out.data) * dt_all / 24]

        ni = (int)(xlim[0]*24 / dt_all)
        ne = (int)(xlim[1]*24 / dt_all)

        cnt = 0
        power_acc = np.zeros_like(self.storage_p[0].data)
        for storage_item in self.storage_p:
            assert storage_item.dt == dt_all
            plt.bar(storage_item.time()[ni:ne]* 1/24, np.maximum(0,storage_item.data[ni:ne]),
                    label = label_list[cnt], width =  dt_all/24,
                    bottom = np.maximum(0,power_acc[ni:ne]))
            power_acc += storage_item.data
            cnt += 1

        for production_item in self.production_p:
            assert production_item.dt == dt_all
            plt.bar(production_item.time()[ni:ne]* 1/24,
                    np.maximum(0 ,production_item.data[ni:ne] + power_acc[ni:ne])
                    - np.maximum(0, power_acc[ni:ne]),
                    label = label_list[cnt], width =  dt_all/24,
                    bottom = np.maximum(0,power_acc[ni:ne]))
            power_acc += production_item.data
            cnt+=1

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # plt.legend()

        # Shrink current axis by 20%
        ax = plt.gca()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
