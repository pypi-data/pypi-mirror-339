""" This library should be used to obtain runtime estimates for applications that use loops. 


Usage Example

if __name__ == '__main__':
    tempo = LoopTimer(numero_total_registros=10)

    tempo.start(2)

    counting = 0
    for i in range(10):
        if i < 2:
            continue
        time.sleep(1)
        tempo.update_loop(i + 1)
        print(tempo)

    print(tempo.stop())

"""

from datetime import datetime, timedelta
import time

class LoopTimer:
    def __init__(self, records_total_number=None):
        if records_total_number is None:
            raise ValueError("The total number of records must be provided.")

        # Items quantity
        self.records_total_number = records_total_number # Total number of records to be processed
        self.init_index = 0 # Index where the loop starts
        self.processed_records = 0

        # Tempo
        self.start_time = 0 #time.time() Start time
        self.elapsed_time = 0
        self.remaining_execution_time = None
        self.end_time = None
    
    def __str__(self):
        return self.summary()

    def summary(self):
        return "\n".join([
            self.progress(progressbar=True, progressbar_length=50),
            self.session_time(),
            self.time_left(),
            self.expected_end(),
            self.average_speed_session()
        ])

    #---------- Loop Control Actions ----------#

    def start(self, init_index: int = 0):
        if self.start_time != 0:
            raise ValueError("This LoopTimer instance cannot be started again before being stopped.")

        if init_index >= self.records_total_number:
            raise ValueError("The initial index cannot be greater than or equal to the total number of records.")  
        


        self.start_time = time.time()
        self.init_index = init_index
    
    def update_loop(self, processed_records: int):
        if self.init_index > processed_records:
            raise ValueError('The initial index must match the value specified in the "start" method attribute.')

        self.processed_records = processed_records
    
    def stop(self, return_summary: bool = True) -> str | None:
        if self.start_time == 0:
            raise ValueError("'Start' method is required.")

        if hasattr(self, 'end_time') and self.end_time is not None:
            raise RuntimeError("Execution has already been finalized.")        
        
        self.end_time = time.time()
        
        if return_summary:
            return self.summary()


    #---------- Progress Display ----------#

    def progress(self,
        prefix: str = 'Progress:',
        suffix: str = 'Complete',
        progressbar: bool = True,
        decimal_places: int = 1,
        formatted_percentage: bool = True,
        progressbar_length: int = 50
    ) -> str:
        """Returns the loop progress percentage."""

        if progressbar and progressbar_length == 0:
            raise ValueError('Argumento "progressbar_length" Obrigatório Caso "progressbar" seja True')
        if self.start_time == 0:
            raise ValueError('You must call the start() method before calling progress().')
        if self.processed_records == 0:
            return 'No records have been processed yet'

        match progressbar:
            case True:
                percent = ("{0:." + str(decimal_places) + "f}").format(100 * (self.processed_records / self.records_total_number))
                filledLength = int(progressbar_length * self.processed_records // self.records_total_number)
                bar = '█' * filledLength + '-' * (progressbar_length - filledLength)
                return f'\r{prefix} |{bar}| {percent}% {suffix}'

            case False:
                percentage = (self.processed_records / self.records_total_number) * 100
                return f"{prefix} {self.processed_records}/{self.records_total_number} ({percentage:.{str(decimal_places)}f}{'%' if formatted_percentage else ''} {suffix})"
        
    def session_time(self, prefix: str = 'Elapsed time (session):', suffix: str = '', epoch_format=False) -> str:
        if self.start_time == 0:
            raise ValueError('You must call the start() method before calling session_time().')
        
        self.__calculate_time_left()
        if epoch_format:
            return self.elapsed_time

        hours = int(self.elapsed_time // 3600)
        minutes = int((self.elapsed_time % 3600) // 60)
        seconds = int(self.elapsed_time % 60)
        return f"{prefix} {hours:02d}:{minutes:02d}:{seconds:02d} {suffix}"

    def time_left(self, prefix: str = 'Remaining time:', suffix: str = '', seconds_format: bool = False) -> str | int | None:
        self.__calculate_time_left()

        if self.remaining_execution_time is None:
            return 
        
        time_left = self.remaining_execution_time - datetime.now()

        if time_left.total_seconds() <= 0:
            return "Time exceeded"

        seconds_left = time_left.total_seconds()
        if seconds_format:
            return int(seconds_left)

        hours = int(seconds_left // 3600)
        minutes = int((seconds_left % 3600) // 60)
        seconds = int(seconds_left % 60)
        return f"{prefix} {hours:02d}:{minutes:02d}:{seconds:02d} {suffix}"

    def expected_end(self, prefix: str = 'Expected end time:', suffix: str = '', datetime_format=False) -> str | None:
        self.__calculate_time_left()

        if self.remaining_execution_time is None:
            return None

        if datetime_format:
            return self.remaining_execution_time
        return f"{prefix} {self.remaining_execution_time.strftime('%H:%M:%S')} {suffix}"
    
    def average_speed_session(self, prefix: str = 'Average speed (records/s):', suffix: str = 'records per second', decimal_places: int = 2, em: str = 's') -> str:

        self.__calculate_time_left()
        if self.elapsed_time > 0:
            processed_records = self.processed_records - self.init_index      

            records = processed_records / self.elapsed_time              
            if em == 's':
                return f"{prefix} {records:.{str(decimal_places)}f} {suffix}" 
            if em == 'm':
                return f"{prefix} {records * 60:.{str(decimal_places)}f} {suffix}"
            if em == 'h':
                return f"{prefix} {records * 3600:.{str(decimal_places)}f} {suffix}"


    #---------- Private Methods ----------#
    def __calculate_time_left(self) -> datetime | None:
        if self.start_time == 0:
            return None

        # Check how much time has passed since execution started
        self.elapsed_time = time.time() - self.start_time

        # Check how many records have been processed since the beginning
        session_records = self.processed_records - self.init_index

        # Calculate average processing speed
        average_speed_session = session_records / self.elapsed_time
        
        records_left = self.records_total_number - self.processed_records

        if average_speed_session > 0:
            time_left = records_left / average_speed_session
        else:
            time_left = float('inf')
        
        if time_left != float('inf'):
            end_time = datetime.now() + timedelta(seconds=time_left)
            self.remaining_execution_time = end_time
        else:
            self.remaining_execution_time = None
        
        return self.remaining_execution_time
