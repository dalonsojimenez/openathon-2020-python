import psutil

class Extractor:

    def __init__(self):
        print('Se ha creado la clase Extractor')

    def get_virtual_memory_percent(self):
        return psutil.virtual_memory()._asdict()['percent']

    def get_cpu_percent(self):
        return psutil.cpu_percent()

    def get_disk_usage_percent(self):
        return psutil.disk_usage('/')._asdict()['percent']
    
    def get_cpu_freq(self): #scpufreq(current=931.42925, min=800.0, max=3500.0)
        return psutil.cpu_freq() 
    
    def get_load_avg(self):
        return [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]