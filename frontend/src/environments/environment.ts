export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'eccweizhi-fsnd.us', // the auth0 domain prefix
    audience: 'myFoobar', // the audience set for the auth0 app
    clientId: 'PtgK7Qhbudtf1ZUWnINHlbWpaKCpgrqT', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
