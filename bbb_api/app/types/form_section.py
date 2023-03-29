from enum import Enum


class FS_FormSection(Enum):
    BASICO = 'BASICO'  # Seção básica do formulário
    PESSOAL = 'PESSOAL'  # Seção pessoal do formulário
    FAMILIA = 'FAMILIA'  # Seção de informações da família do formulário
    ESTILODEVIDA = 'ESTILODEVIDA'  # Seção de informações de estilo de vida do formulário
    DESEJOS = 'DESEJOS'  # Seção de informações de desejos do formulário
    MEDICO = 'MEDICO'  # Seção de informações médicas do formulário
    BBB = 'BBB'  # Seção específica do Big Brother Brasil do formulário
