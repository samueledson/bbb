export const constants = {
  URL_API: 'http://localhost:8000',
	SEASON: 'BBB24',
  APPLICATION_STATUS: {
    PENDENTE: 'PENDENTE',
    ENTREGUE: 'ENTREGUE',
  }
};

export const api = {
  candidates: {
    login: `${constants.URL_API}/candidates/login`,
    create: `${constants.URL_API}/candidates`,
    update: `${constants.URL_API}/candidates/:candidate_id`,
    delete: `${constants.URL_API}/candidates/:candidate_id`,
    get_application: `${constants.URL_API}/candidates/:candidate_id/applications/:program_season`,
  },
  applications: {
    //read: `${constants.URL_API}/applications/:application_id`,
    create: `${constants.URL_API}/applications`,
    update: `${constants.URL_API}/applications/:application_id`,
    delete: `${constants.URL_API}/applications/:application_id`,
    answers: {
      get_all: `${constants.URL_API}/applications/:application_id/answers`,
      create: `${constants.URL_API}/applications/:application_id/answers`,
      update: `${constants.URL_API}/applications/:application_id/answers`,
    }
  },
	questions_program_season: `${constants.URL_API}/questions`,
};
