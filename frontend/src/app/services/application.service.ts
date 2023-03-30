import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { api } from 'src/config';

@Injectable({
	providedIn: 'root',
})
export class ApplicationService {
	constructor(private _http: HttpClient) {}

  create(candidate_id: number, data: any) {
    const body = {
      candidate_id: candidate_id,
      ...data
    }
    return this._http.post(`${api.applications.create}`, body);
  }

  update(application_id: number, body: any) {
    return this._http.put(`${api.applications.update.replace(':application_id', application_id.toString())}`, body);
  }

  delete(application_id: number) {
    return this._http.delete(`${api.applications.delete.replace(':application_id', application_id.toString())}`);
  }

  getAnswers(application_id: number) {
    return this._http.get(`${api.applications.answers.get_all.replace(':application_id', application_id.toString())}`);
  }

  postAnswers(application_id: number, body: any) {
    return this._http.post(`${api.applications.answers.create.replace(':application_id', application_id.toString())}`, body);
  }

}
