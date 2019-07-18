import numpy as np


# Todo: -Improve return values
#       -Implement the ability to solve a tp with more stages than one
#       -Add MODI method
#       -Helper function for calculating transport amount
#       -Building useful class
#       -Implement tests
#       -Finding python style guides to improve code
#       -Exception handling

class Solver(object):

    def __init__(self, s_v, d_v, c_m):
        self.supply_vector = s_v
        self.demand_vector = d_v
        self.cost_matrix = c_m
        self.transport_matrix = np.zeros((s_v.size, d_v.size))


    def nwc_rule(self):
        j = 0
        i = 0
        s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp = self.__surplus()

        while j < d_v_tmp.size and i < s_v_tmp.size:
            if d_v_tmp[j] >= s_v_tmp[i]:
                amount = s_v_tmp[i]
                # print("Demand is bigger", amount)
            else:
                amount = d_v_tmp[j]
                # print("Supply is bigger", amount)

            d_v_tmp[j] = d_v_tmp[j] - amount
            s_v_tmp[i] = s_v_tmp[i] - amount
            t_m_tmp[i][j] = amount

            if s_v_tmp[i] == 0:
                i += 1
            else:
                j += 1

        total_costs, surplus = self.__costs(t_m_tmp)

        return t_m_tmp, total_costs, surplus

    def cm_rule(self):
        s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp = self.__surplus()

        columns = list(range(0, d_v_tmp.size))
        rows = list(range(0, s_v_tmp.size))
        infinity = np.inf

        while len(columns) > 0:

            j = min(columns)

            tmp = c_m_tmp[:, j]
            tmp = tmp.tolist()

            minima = min(tmp)
            i = tmp.index(minima)

            while i not in rows:

                if self.surplus == "demand" and len(rows) == 1:
                    i = s_v_tmp.size - 1
                    break

                tmp[i] = infinity
                minima = min(tmp)
                i = tmp.index(minima)

                if not rows:
                    break

            if d_v_tmp[j] >= s_v_tmp[i]:
                amount = s_v_tmp[i]
                # print("Demand is bigger", amount)
            else:
                amount = d_v_tmp[j]
                # print("Supply  is bigger", amount)

            d_v_tmp[j] = d_v_tmp[j] - amount
            s_v_tmp[i] = s_v_tmp[i] - amount
            t_m_tmp[i][j] = amount

            if s_v_tmp[i] == 0 or (np.sum(d_v_tmp) == 0 and s_v_tmp[i] == infinity):
                rows.remove(i)

            # to avoid loop if there is an supply surplus
            if d_v_tmp[j] == 0 or (np.sum(s_v_tmp) == 0 and d_v_tmp[j] == infinity):
                columns.remove(j)

        total_costs, surplus = self.__costs(t_m_tmp, c_m_tmp)

        return t_m_tmp, total_costs, surplus

    def __costs(self, transport_matrix):
        surplus = 0
        transport_matrix = np.copy(transport_matrix)

        if self.surplus == "demand":
            surplus = np.sum(transport_matrix[-1, :])
            surplus = surplus * -1
            transport_matrix = np.delete(transport_matrix, -1, axis=0)

        if self.surplus == "supply":
            surplus = np.sum(transport_matrix[:, -1])
            transport_matrix = np.delete(transport_matrix, -1, axis=1)

        tmp = np.multiply(transport_matrix, self.cost_matrix)

        return tmp.sum(), surplus

    def __surplus(self):
        s_v_tmp = np.copy(self.supply_vector)
        d_v_tmp = np.copy(self.demand_vector)
        t_m_tmp = np.copy(self.transport_matrix)
        c_m_tmp = np.copy(self.cost_matrix)

        infinity = np.inf

        # Supply surplus, add entry to demand vector and column to cost- and transport matrix
        if np.sum(s_v_tmp) > np.sum(d_v_tmp):
            d_v_tmp = np.append(d_v_tmp, infinity)
            new_column_tmp = np.zeros((s_v_tmp.size, 1))
            t_m_tmp = np.append(t_m_tmp, new_column_tmp, axis=1)
            c_m_tmp = np.append(c_m_tmp, new_column_tmp, axis=1)
            self.surplus = "supply"

        # Demand surplus, add entry supply vector and row to cost- and transport matrix
        elif np.sum(s_v_tmp) < np.sum(d_v_tmp):
            s_v_tmp = np.append(s_v_tmp, infinity)
            new_row_t_tmp = np.zeros((1, d_v_tmp.size))
            new_row_c_tmp = np.full((1, d_v_tmp.size), infinity)
            t_m_tmp = np.append(t_m_tmp, new_row_t_tmp, axis=0)
            c_m_tmp = np.append(c_m_tmp, new_row_c_tmp, axis=0)
            self.surplus = "demand"

        else:
            self.surplus = "equal"

        return s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp



def main():
    supply_vector = np.array([20, 40, 30])
    demand_vector = np.array([20, 20, 20, 15, 15])
    cost_matrix = np.array([[10, 15, 9, 13, 12],
                            [11, 30, 4, 13, 12],
                            [12, 13, 4, 1, 122]])

    # Debug
    print("Debug")

    problem = Solver(supply_vector, demand_vector, cost_matrix)

    # Test column minima rule
    matrix, costs, surplus = problem.cm_rule()
    print("Column Minima Rule")
    print("Matrix: \n ", matrix)
    print("Total costs: \n ", costs)
    print("Surplus in units: ", surplus)

    # Test north west corner rule
    matrix, costs = problem.nwc_rule()
    print("North West Corner Rule")
    print("Matrix: \n", matrix)
    print("Total costs: ", costs)
    print("Surplus in units: ", surplus)




if __name__ == "__main__":
    main()
