import json, re
from uuid import UUID
from datetime import date
from src.utils.transfer import Transfer
from src.policies.auth import AuthPolicy
from typing import Tuple, Type, List, Any


class BaseValidator:

    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_body(body) -> Transfer:
        '''
        Verifica se o argumento passado pode ser convertido para um dicionário,
        sendo possível identificar uma requisição enviada em formato JSON.
        '''
        res = Transfer()
        try:
            json.loads(body)
            res.set_status_code(200)
        except BaseException as e:
            res.set_status_code(400)
            res.set_message("O corpo informado não é um json válido")
        finally:
            return res
        
    @staticmethod
    def validate_required_fields(body: dict, fields: List[Tuple[str, Type]]) -> Transfer:
        '''
        Executa a validação de campos obrigatórios em um dicionário.
        
        Argumentos:
        body: dicionário obtido pela requisição (formato JSON)
        fields: lista de tuplas, onde a primeira posição é o nome do campo e o segundo é o tipo
        '''
        res = Transfer()
        for field, _type in fields:
            if field not in body.keys():
                res.set_status_code(400)
                res.set_message(f"O campo obrigatório '{field}' não foi encontrado")
                break
            
            if type(body[field]) != _type:
                res.set_status_code(400)
                res.set_message(f"O campo '{field}' deve ser do tipo {_type.__name__}")
                break

        return res
        

    @staticmethod
    def validate_optional_field(body: dict, fields: List[Tuple[str, Type, Any]]) -> Transfer:
        '''
        Executa a validação de campos opcionais em um dicionário.
        
        Argumentos:
        body: dicionário obtido pela requisição (formato JSON)
        fields: lista de tuplas, onde a primeira posição é o nome do campo, o segundo é
        o tipo e o terceiro é o valor default
        '''
        res = Transfer()
        for field, _type, default in fields:
            if field not in body.keys():
                body[field] = default

            if body[field] is not None and type(body[field]) != _type:
                res.set_status_code(400)
                res.set_message(f"O campo '{field}' deve ser do tipo {_type.__name__}")
                break

        return res
    
    @staticmethod
    def validate_list_of_dict(array: List[dict], fields: List[Tuple[str, Type]]) -> Transfer:
        '''
        Verifica se uma listagem de elementos em formato JSON possui os campos e tipos especificados.

        Argumentos:
        array: lista de dicionários que será avaliada
        fields: lista de tuplas em que a primeira posição é o nome do campo e o segundo o tipo
        '''
        res = Transfer()
        for element in array:
            for field, _type in fields:
                if field not in element.keys():
                    res.set_status_code(400)
                    res.set_message(f"O campo '{field}' não está presente na listagem")
                    break

                if type(element[field]) != _type:
                    res.set_status_code(400)
                    res.set_message(f"O campo {field} deve ser do tipo {_type.__name__}")
                    break
            
            if res.get_status_code() == 400:
                break

        return res
    
    @staticmethod
    def validate_uuid(value: str) -> Transfer:
        '''Verifica se a string informada está no formato de uuid utilizado pelo sistema.'''
        res = Transfer()
        try:
            UUID(value)
            res.set_status_code(200)
        except BaseException as e:
            res.set_status_code(400)
            res.set_message("O id informado não é válido")
        finally:
            return res
        
    @staticmethod
    def validate_jwt(token: str) -> Transfer:
        '''Verifica se um token de autenticação informado possui o formato correto JWT.'''
        return AuthPolicy.is_jwt(token)
    
    @staticmethod
    def validate_email(email: str) -> Transfer:
        '''Verifica se a string informada está no formato de um e-mail válido.'''
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        res = Transfer()

        if re.fullmatch(regex, email):
            res.set_status_code(200)
        else:
            res.set_status_code(400)
            res.set_message("O e-mail informado não é válido")

        return res
    
    @staticmethod
    def validate_string_len(value: str, lmin=None, lmax=None) -> Transfer:
        '''
        Valida se uma string possui um tamanho mínimo ou máximo. Se None for passado, ignora
        limite na dimensão.

        Argumentos:
        lmin: Valor inteiro para o tamanho mínimo ou None para não avaliar mínimo
        lmax: Valor inteiro para o tamanho máximo ou None para não avaliar máximo
        '''
        res = Transfer()
        try:
            if lmin is not None and lmax is not None and lmin > lmax:
                raise Exception("O limite máximo precisar ser maior que o limite mínimo")
            
            if lmin is not None and len(value) < lmin:
                raise Exception(f"O campo precisa ter ao menos {lmin} caracteres")
            
            if lmax is not None and len(value) > lmax:
                raise Exception(f"O campo não pode ter mais que {lmax} caracteres")
            
        except BaseException as e:
            res.set_status_code(400)
            res.set_message(str(e))

        finally:
            return res
        
    @staticmethod
    def validate_interval_value(value: float, lmin=None, lmax=None) -> Transfer:
        '''
        Valida se um número está entre um intervalo mínimo e máximo. Se None for passado,
        ignora limite na dimensão.

        Argumentos:
        lmin: Valor mínimo ou None para não avaliar mínimo
        lmax: Valor máximo ou None para não avaliar máximo
        '''
        res = Transfer()
        try:
            if lmin is not None and lmax is not None and lmin > lmax:
                raise Exception("O valor máximo precisar ser maior que o valor mínimo")
            
            if lmin is not None and value < lmin:
                raise Exception(f"O valor não pode ser menor que {lmin}")
            
            if lmax is not None and value > lmax:
                raise Exception(f"O valor não pode ser maior que {lmax}")
            
        except BaseException as e:
            res.set_status_code(400)
            res.set_message(str(e))

        finally:
            return res
        
    @staticmethod
    def validate_date_string(value: str) -> Transfer:
        res = Transfer()
        try:
            date.fromisoformat(value)
        except:
            res.set_status_code(400)
            res.set_message("Uma data precisa estar no formato yyyy-mm-dd")
        finally:
            return res
