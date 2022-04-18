export const BACKEND_DOCKER_URL = 'http://web-server'
export const BACKEND_LOCAL_URL = 'http://localhost:8888'

export const ADMIN_USER =  {
    name: process.env.ADMIN_ACCOUNT,
    password: process.env.ADMIN_PASSWORD
};

export const ASSIGNMENT_STATE_NAME = {
  1 : 'ALIVE',
  2 : 'DEAD'
}

export const SUBMISSION_STATE_NAME = {
  1 : 'NORMAL',
  2 : 'DANGER',
  3 : 'SUBMITTED',
  4 : 'EXPIRED'
}
