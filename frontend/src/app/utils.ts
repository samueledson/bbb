import { HttpErrorResponse } from "@angular/common/http";
import { throwError } from "rxjs";

export function handleError(error: HttpErrorResponse) {
  if (error.status === 401) {
    // Executa uma ação personalizada para lidar com o erro 401
    console.error('As credenciais fornecidas são inválidas.');
  } else {
    // Executa outra ação personalizada para lidar com outros tipos de erro
    console.error('Ocorreu um erro ao processar a solicitação:', error.message);
  }
  // Lança o erro para que ele seja tratado por outros observadores
  return throwError('Algo deu errado. Tente novamente mais tarde.');
}
