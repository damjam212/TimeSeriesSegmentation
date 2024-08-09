import plotly.express as px
import ruptures as rpt
from tqdm import tqdm
import numpy as np

class BenchmarkCaller():
    # def __init__(self, experiments_number, algorithms_number, algorithms_tags):
    #     self.experiments_number = experiments_number
    #     self.history = []
    #     self.algorithms_number = algorithms_number
    #     self.ranksSum = np.zeros(algorithms_number)
    #     self.experiments_conducted = 0 
    #     self.algorithms_tags = algorithms_tags

    def __init__(self, itr, custom_parameter):
        self.result_matrix = np.zeros((10, 7, 4 ,itr, custom_parameter), dtype = float)
        self.experiments = []
        self.itr = itr
        self.custom_parameter = custom_parameter
    def register_experiment(self,function):
        self.experiments.append(function)
        
    def call_experiments(self, seed, iteration, custom_parameter, parameter_number):
        i = 0 
        for fun in (self.experiments):
            all_evals, data, original_points = fun(seed, custom_parameter)
            for index_alg, eval in enumerate(all_evals):
                for index_metric, row in eval.iterrows():
                    self.result_matrix[i, index_metric, index_alg, iteration, parameter_number] = row[1]
            i = i+1
            #for e in all_evals:
            #    print(e)
            #rpt.display(data, original_points)
    # def add_experiment(self, results):
    #     if self.experiments_conducted == self.experiments_number:
    #         raise ValueError("Niewłaściwa wartość")
    #     self.experiments_conducted += 1
    #     sorted_indices = np.argsort(results)[::-1] + 1
    #     self.ranksSum += sorted_indices
    #     if self.experiments_conducted == self.experiments_number:
    #         self.print_current_results()

    def get_matrix_results(self):
        return self.result_matrix
        
    def add_experiment(self, results):
        if self.experiments_conducted == self.experiments_number:
            print("Niewłaściwa wartość")
        else:
            #sorted_indices = np.argsort(results)[::-1] + 1

            order = results.argsort()[::-1]
            sorted_indices = order.argsort()+ 1
            self.ranksSum += sorted_indices
            self.history.append(sorted_indices)
            self.experiments_conducted += 1
            if self.experiments_conducted == self.experiments_number:
                self.print_current_results()       
            
    def print_current_results(self):
        print("Conducted experimets: "+str(self.experiments_conducted))

        # x = []
        # y = []

        # df = pd.DataFrame(self.history)
        # for i, array in enumerate(self.history):
        #     x.extend([i] * len(array))  # Współrzędne x (wszystkie elementy mają taką samą współrzędną x)
        #     y.extend(array)  # Współrzędne y (wartości z tablicy)
        
        # # Tworzenie scatter plot
        # plt.scatter(x, y)
        
        # # Opcjonalne etykiety osi
        # plt.xlabel('Index of array in list')
        # plt.ylabel('Values in arrays')
        
        # Wyświetlenie scatter plot
        plt.show()
        for i in range(self.algorithms_number):
            print(self.algorithms_tags[i]+" current average rank is: "+str((float(self.ranksSum[i])/ self.experiments_conducted)))
                    
# arr = np.array([3,4,16])
# print(np.argsort(arr[::-1]))

        
        