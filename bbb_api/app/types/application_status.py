from enum import Enum


class ApplicationStatus(Enum):
    PENDENTE = 'PENDENTE'
    ENTREGUE = 'ENTREGUE'
    REJEITADO = 'REJEITADO'
    APROVADO = 'APROVADO'

