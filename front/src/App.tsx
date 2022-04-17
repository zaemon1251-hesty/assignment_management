/* eslint-disable react/button-has-type */
/* eslint-disable camelcase */
import { useState, ReactElement } from 'react'
import axios from 'axios'
import {DefaultService, Body_create_token_api_users_login_post, Submission } from './api/client'
import logo from './logo.svg'
import '../styles/App.css'
import { ADMIN_USER, BACKEND_DOCKER_URL } from './constants'

axios.interceptors.request.use(
  // allowedOriginと通信するときにトークンを付与するようにする設定
  (config) => {
    const newConfig = { ...config }
    const { origin } = new URL(config.url as string)
    const allowedOrigins = [BACKEND_DOCKER_URL]
    const token = localStorage.getItem('token')
    if (allowedOrigins.includes(origin) && token) {
      newConfig.headers = config.headers || {}
      newConfig.headers.Authorization = token
    }
    return newConfig;
  },
  (error) => Promise.reject(error)
)

function App(): ReactElement  {
  const storedJwt = localStorage.getItem('token')
  const [jwt, setJwt] = useState(storedJwt || null)
  const [submissions, setSubmissions] = useState<Submission[]>([])
  const [fetchError, setFetchError] = useState<unknown>(null)
  
  const getJwt = async () => {
    try {
      const token = await DefaultService.createTokenApiUsersLoginPost(ADMIN_USER as Body_create_token_api_users_login_post)
      localStorage.setItem('token', token.access_token)
      setJwt(token.access_token)  
    } catch (err) {
      setFetchError(err)
    }
  }

  const getSubs = async () => {
    try {
      const data = await DefaultService.getAllApiSubmissionsGet(1)
      setSubmissions(data)
      setFetchError(null)
    } catch (err) {
      setFetchError(err)
    }
  }
  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
      </header>
      <section style={{ marginBottom: '10px' }}>
        <button onClick={
          () => {
            void (async () => {
              await getJwt();
            })();
          }
        }>Get JWT</button>
        {jwt && (
          <pre>
            <code>{jwt}</code>
          </pre>
        )}
      </section>
      <section>
        <button onClick={
          () => {
            void (async () => {
              await getSubs();
            })();
          }
        }>Get subs</button>
        <ul>
          {submissions.map((submission) => (
            <li>{submission.state}</li>
          ))}
        </ul>
        {fetchError && <p style={{ color: 'red' }}>{fetchError as string}</p>}
      </section>
    </div>
  )
}

export default App;
