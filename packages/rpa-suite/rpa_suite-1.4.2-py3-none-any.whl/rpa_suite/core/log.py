from typing import Optional as Op
from ..functions.__create_log_dir import _create_log_dir
from rpa_suite.functions._printer import error_print, alert_print
from loguru import logger
import sys, os, inspect


class Filters():
    """
    Class that provides utilities for filtering log messages based on specific keywords.

    This class allows you to define a list of words that, if found in a log message, will trigger a modification of that message. 
    The modified message will indicate that it has been altered due to the presence of a filtered word.

    Methods:
        __call__: Checks if any of the specified words are present in the log message and alters the message if a match is found.

    Example:
        >>> filter = Filters()
        >>> filter.word_filter = ['error', 'warning']
        >>> record = {"message": "This is an error message."}
        >>> filter(record)  # This will alter the message to 'Log Alterado devido a palavra Filtrada!'

    pt-br
    ----------
    Classe que fornece utilitários para filtrar mensagens de log com base em palavras-chave específicas.

    Esta classe permite que você defina uma lista de palavras que, se encontradas em uma mensagem de log, acionarão uma modificação dessa mensagem. 
    A mensagem modificada indicará que foi alterada devido à presença de uma palavra filtrada.

    Métodos:
        __call__: Verifica se alguma das palavras especificadas está presente na mensagem de log e altera a mensagem se uma correspondência for encontrada.

    Exemplo:
        >>> filtro = Filters()
        >>> filtro.word_filter = ['erro', 'aviso']
        >>> registro = {"message": "Esta é uma mensagem de erro."}
        >>> filtro(registro)  # Isso alterará a mensagem para 'Log Alterado devido a palavra Filtrada!'
    """

    word_filter: Op[list[str]]

    def __call__(self, record):

        if len(self.word_filter) > 0:

            for words in self.word_filter:

                string_words: list[str] = [str(word) for word in words]

                for word in string_words:
                    if word in record["message"]:
                        record["message"] = 'Log Alterado devido a palavra Filtrada!'
                        return True

        return True


class CustomHandler():
    """
    Class that provides a custom logging handler to manage log messages.
    
    This class allows for the formatting and writing of log messages to a specified output. 
    It utilizes a custom formatter to structure the log messages, including details such as 
    the time of logging, log level, and the message itself.

    Methods:
        write: Writes the formatted log message to the output.

    Example:
        >>> handler = CustomHandler(formatter=CustomFormatter())
        >>> handler.write({"time": "12:00", "level": "INFO", "message": "This is a log message."})

    pt-br
    ----------
    Classe que fornece um manipulador de log personalizado para gerenciar mensagens de log.
    
    Esta classe permite a formatação e escrita de mensagens de log em uma saída especificada. 
    Ela utiliza um formatador personalizado para estruturar as mensagens de log, incluindo detalhes como 
    o horário do log, nível de log e a própria mensagem.

    Métodos:
        write: Escreve a mensagem de log formatada na saída.

    Exemplo:
        >>> manipulador = CustomHandler(formatter=CustomFormatter())
        >>> manipulador.write({"time": "12:00", "level": "INFO", "message": "Esta é uma mensagem de log."})
    """
    def __init__(self, formatter):
        self.formatter = formatter

    def write(self, message):
        frame = inspect.currentframe().f_back.f_back
        log_msg = self.formatter.format(message, frame)
        sys.stderr.write(log_msg)


class CustomFormatter:
    """
    Class that provides a custom formatter for log messages.
    
    This class is responsible for formatting log messages in a structured way, 
    allowing for easy readability and understanding of log entries. It formats 
    the log messages to include details such as the time of logging, log level, 
    the filename, line number, and the actual log message.

    Methods:
        format: Formats the log message based on the provided record.

    Example:
        >>> formatter = CustomFormatter()
        >>> log_message = formatter.format({
        ...     "time": "12:00",
        ...     "level": "INFO",
        ...     "message": "This is a log message."
        ... })
        >>> print(log_message)

    pt-br
    ----------
    Classe que fornece um formatador personalizado para mensagens de log.
    
    Esta classe é responsável por formatar mensagens de log de maneira estruturada, 
    permitindo fácil leitura e compreensão das entradas de log. Ela formata 
    as mensagens de log para incluir detalhes como o horário do log, nível de log, 
    o nome do arquivo, número da linha e a mensagem de log real.

    Métodos:
        format: Formata a mensagem de log com base no registro fornecido.

    Exemplo:
        >>> formatador = CustomFormatter()
        >>> mensagem_log = formatador.format({
        ...     "time": "12:00",
        ...     "level": "INFO",
        ...     "message": "Esta é uma mensagem de log."
        ... })
        >>> print(mensagem_log)
    """
    def format(self, record):

        frame = inspect.currentframe().f_back
        full_path_filename = frame.f_code.co_filename

        # Obtenha o nome do arquivo e o nome da pasta
        filename = os.path.basename(full_path_filename)
        foldername = os.path.basename(os.path.dirname(full_path_filename))

        # Combine o nome da pasta e o nome do arquivo
        filename = os.path.join(foldername, filename)
        lineno = frame.f_lineno

        # Formate a mensagem de log TERMINAL
        format_string = "<green>{time:DD.MM.YY.HH:mm}</green> <level>{level: <8}</level> <level>{message}</level>\n"

        log_msg = format_string.format(
            time=record["time"],
            level=record["level"].name,
            filename=filename,
            lineno=lineno,
            message=record["message"]
        )
        return log_msg




class Log():

    """
    Class that provides utilities for logging messages in a structured manner.
    
    This class is responsible for managing log entries, allowing for easy tracking 
    and debugging of application behavior. It supports various logging levels and 
    can be configured to log messages to different outputs, such as files or the console.

    Methods:
        config_logger: Configures the logger with specified parameters.
        
    Example:
        >>> logger = Log()
        >>> logger.config_logger(path_dir='logs', name_log_dir='my_logs', name_file_log='app_log')
    
    pt-br
    ----------
    Classe que fornece utilitários para registrar mensagens de forma estruturada.
    
    Esta classe é responsável por gerenciar entradas de log, permitindo fácil rastreamento 
    e depuração do comportamento da aplicação. Suporta vários níveis de log e 
    pode ser configurada para registrar mensagens em diferentes saídas, como arquivos ou console.

    Métodos:
        config_logger: Configura o logger com parâmetros especificados.
        
    Exemplo:
        >>> logger = Log()
        >>> logger.config_logger(path_dir='logs', name_log_dir='meus_logs', name_file_log='log_app')
    """
    
    filters: Filters
    custom_handler: CustomHandler
    custom_formatter: CustomFormatter
    
    
    def __init__(self):
        ...
    
    def config_logger(self,
                        path_dir:str = None, 
                        name_log_dir:str = None, 
                        name_file_log: str = 'log', 
                        use_default_path_and_name: bool = True, 
                        filter_words: list[str] = None):

        """
        Função responsável por criar um objeto logger com fileHandler e streamHandler
        
        pt-br
        ----------
        Function responsible for create a object logger with fileHandler and streamHandler
        """

        try:

            if not use_default_path_and_name:
                result_tryed: dict = _create_log_dir(path_dir, name_log_dir)
                path_dir = result_tryed['path_created']
            else:
                if path_dir == None and name_log_dir == None:
                    result_tryed: dict = _create_log_dir()
                    path_dir = result_tryed['path_created']


            # ATRIBUIÇÕES
            new_filter: Op[Filters] = None
            if filter_words is not None:
                new_filter: Filters = Filters()
                new_filter.word_filter = [filter_words]


            # configuração de objetos logger
            file_handler = fr'{path_dir}\{name_file_log}.log'
            logger.remove()

            # Formate a mensagem de log FILE
            log_format: str = "<green>{time:DD.MM.YY.HH:mm}</green> <level>{level: <8}</level> <green>{extra[filename]}</green>:{extra[lineno]: <4} <level>{message}</level>"


            formatter = CustomFormatter()
            if new_filter is not None:
                logger.add(file_handler, filter=new_filter, level="DEBUG", format=log_format)
            else:
                logger.add(file_handler, level="DEBUG", format=log_format)

            # Adicione sys.stderr como um manipulador
            logger.add(sys.stderr, level="DEBUG", format=formatter.format)

            return file_handler

        except Exception as e:

            error_print(f'Houve um erro durante a execução da função: {self.config_logger.__name__}! Error: {str(e)}.')
            return None
    


    def log_start_run_debug(self,
                            msg_start_loggin: str) -> None: # represent start application

        """
        Function responsable to generate ``start run log level debug``, in file and print on terminal the same log captured on this call.
        
        pt-br
        ----------
        Função responsável por gerar o nível de log ``início execução nível debug``, em arquivo e imprimir no terminal o mesmo log capturado nesta chamada.
        """

        file_h: False

        try:
            file_h = self.config_logger()

        except Exception as e:

            error_print(f'Para usar o log_start_run_debug é necessario instanciar file_handler usando o arquivo "logger_uru" em algum arquivo de configuração do seu projeto primeiramente! Error: {str(e)}')

        try:
            try:
                if file_h:
                    with open(file_h, 'a') as f:
                        f.write('\n')

            except Exception as e:
                alert_print(f'Não foi possivel gerar break_row para log inicial!')

            # logger.debug(f'{msg_start_loggin}')
            frame = inspect.currentframe().f_back
            full_path_filename = frame.f_code.co_filename

            # Obtenha o nome do arquivo e o nome da pasta
            filename = os.path.basename(full_path_filename)
            foldername = os.path.basename(os.path.dirname(full_path_filename))

            # Combine o nome da pasta e o nome do arquivo
            filename = os.path.join(foldername, filename)
            lineno = frame.f_lineno

            # Vincule o nome do arquivo e a linha à mensagem de log
            logger.bind(filename=filename, lineno=lineno).debug(f'{msg_start_loggin}')

        except Exception as e:
            error_print(f'Erro durante a função: {self.log_start_run_debug.__name__}! Error: {str(e)}')


    def log_debug(
                self,
                msg: str) -> None:

        """
        Function responsable to generate log level ``debug``, in file and print on terminal the same log captured on this call.
        
        pt-br
        -----
        Função responsável por gerar o nível de log ``debug``, em arquivo e imprimir no terminal o mesmo log capturado nesta chamada.
        """

        try:
            frame = inspect.currentframe().f_back
            full_path_filename = frame.f_code.co_filename

            # Obtenha o nome do arquivo e o nome da pasta
            filename = os.path.basename(full_path_filename)
            foldername = os.path.basename(os.path.dirname(full_path_filename))

            # Combine o nome da pasta e o nome do arquivo
            filename = os.path.join(foldername, filename)
            lineno = frame.f_lineno

            # Vincule o nome do arquivo e a linha à mensagem de log
            logger.bind(filename=filename, lineno=lineno).debug(msg)

        except Exception as e:
            error_print(f'Erro durante a função: {self.log_debug.__name__}! Error: {str(e)}')

    def log_info(
                self,
                msg: str) -> None:

        """
        Function responsable to generate log level ``info``, in file and print on terminal the same log captured on this call.
        
        pt-br
        -----
        Função responsável por gerar o nível de log ``info``, em arquivo e imprimir no terminal o mesmo log capturado nesta chamada.
        """

        try:
            frame = inspect.currentframe().f_back
            full_path_filename = frame.f_code.co_filename

            # Obtenha o nome do arquivo e o nome da pasta
            filename = os.path.basename(full_path_filename)
            foldername = os.path.basename(os.path.dirname(full_path_filename))

            # Combine o nome da pasta e o nome do arquivo
            filename = os.path.join(foldername, filename)
            lineno = frame.f_lineno

            # Vincule o nome do arquivo e a linha à mensagem de log
            logger.bind(filename=filename, lineno=lineno).info(msg)

        except Exception as e:
            error_print(f'Erro durante a função: {self.log_info.__name__}! Error: {str(e)}')

    def log_warning(self, 
                    msg: str) -> None:

        """
        Function responsable to generate log level ``warning``, in file and print on terminal the same log captured on this call.
        
        pt-br
        -----
        Função responsável por gerar o nível de log ``aviso``, em arquivo e imprimir no terminal o mesmo log capturado nesta chamada.
        """

        try:
            frame = inspect.currentframe().f_back
            full_path_filename = frame.f_code.co_filename

            # Obtenha o nome do arquivo e o nome da pasta
            filename = os.path.basename(full_path_filename)
            foldername = os.path.basename(os.path.dirname(full_path_filename))

            # Combine o nome da pasta e o nome do arquivo
            filename = os.path.join(foldername, filename)
            lineno = frame.f_lineno

            # Vincule o nome do arquivo e a linha à mensagem de log
            logger.bind(filename=filename, lineno=lineno).warning(msg)

        except Exception as e:
            error_print(f'Erro durante a função: {self.log_warning.__name__}! Error: {str(e)}')


    def log_error(
                self, 
                msg: str) -> None:

        """
        Function responsable to generate log level ``error``, in file and print on terminal the same log captured on this call.
        
        pt-br
        -----
        Função responsável por gerar o nível de log ``erro``, em arquivo e imprimir no terminal o mesmo log capturado nesta chamada.
        """

        try:
            frame = inspect.currentframe().f_back
            full_path_filename = frame.f_code.co_filename

            # Obtenha o nome do arquivo e o nome da pasta
            filename = os.path.basename(full_path_filename)
            foldername = os.path.basename(os.path.dirname(full_path_filename))

            # Combine o nome da pasta e o nome do arquivo
            filename = os.path.join(foldername, filename)
            lineno = frame.f_lineno

            # Vincule o nome do arquivo e a linha à mensagem de log
            logger.bind(filename=filename, lineno=lineno).error(msg)

        except Exception as e:
            error_print(f'Erro durante a função: {self.log_error.__name__}! Error: {str(e)}')


    def log_critical(self, 
                    msg: str) -> None:

        """
        Function responsable to generate log level ``critical``, in file and print on terminal the same log captured on this call.
        
        pt-br
        ----------
        
        Função responsável por gerar o nível de log ``crítico``, em arquivo e imprimir no terminal o mesmo log capturado nesta chamada.
        """

        try:
            frame = inspect.currentframe().f_back
            full_path_filename = frame.f_code.co_filename

            # Obtenha o nome do arquivo e o nome da pasta
            filename = os.path.basename(full_path_filename)
            foldername = os.path.basename(os.path.dirname(full_path_filename))

            # Combine o nome da pasta e o nome do arquivo
            filename = os.path.join(foldername, filename)
            lineno = frame.f_lineno

            # Vincule o nome do arquivo e a linha à mensagem de log
            logger.bind(filename=filename, lineno=lineno).critical(msg)

        except Exception as e:
            error_print(f'Erro durante a função: {self.log_critical.__name__}! Error: {str(e)}')

