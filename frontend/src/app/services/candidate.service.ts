import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { api } from 'src/config';

@Injectable({
	providedIn: 'root',
})
export class CandidateService {
	constructor(private _http: HttpClient) {}

	login(cpf: string, password: string) {
    const body = {
      cpf: cpf,
      password: password
    }
    return this._http.post(`${api.candidates.login}`, body);
  }

  create(body: any) {
    return this._http.post(`${api.candidates.create}`, body);
  }

  update(candidate_id: number, body: any) {
    return this._http.put(`${api.candidates.update.replace(':candidate_id', candidate_id.toString())}`, body);
  }

  delete(candidate_id: number) {
    return this._http.delete(`${api.candidates.delete.replace(':candidate_id', candidate_id.toString())}`);
  }

  getApplication(candidate_id: number, program_season: string) {
    return this._http.get(`${api.candidates.get_application.replace(':candidate_id', candidate_id.toString()).replace(':program_season', program_season)}`);
  }

}
