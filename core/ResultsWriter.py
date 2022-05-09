from datetime import datetime
import os

class ResultsWriter:
    def __init__(self):
        self.maindir_path = os.path.dirname(os.path.split(__file__)[0])
        self.results_dir = self.get_datetime()


    def get_datetime(self):
        now = datetime.now()
        datetime_now = now.strftime("[%d.%m.%Y]_[%H.%M.%S]")
        result_dir_path = os.path.join(self.maindir_path, 'results', datetime_now)
        if not os.path.exists(result_dir_path):
            os.makedirs(result_dir_path)
            open(os.path.join(result_dir_path, 'good.txt'), 'a').close()
        return result_dir_path

    def write_to_file(self,  log: str):
        path = os.path.join(self.results_dir, 'good.txt')
        with open(path, 'a+', encoding='utf-8', errors='ignore') as f:
            f.write(log + '\n')


if __name__ == '__main__':
    ResultsWriter()