import { useState, VFC } from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import { BACKEND_DOCKER_URL } from './constants';


axios.interceptors.request.use(
  // allowedOriginと通信するときにトークンを付与するようにする設定
  config => {
    const { origin } = new URL(config.url as string);
    const allowedOrigins = [BACKEND_DOCKER_URL];
    const token = localStorage.getItem('token');
    if (!config.headers) {
      config.headers = {};
    }
    if (allowedOrigins.includes(origin)) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

type Food = {
  id: number
  description: string
}


const App:VFC = () => {
  const storedJwt = localStorage.getItem('token');
  const [jwt, setJwt] = useState(storedJwt || null);
  const [foods, setFoods] = useState<Food[]>([]);
  const [fetchError, setFetchError] = useState(null);
  
  const getJwt = async () => {
    const { data } = await axios.get(`${BACKEND_DOCKER_URL}/login`);
    localStorage.setItem('token', data.token);
    setJwt(data.token);
  };

  const getFoods = async () => {
    try {
      const { data } = await axios.get(`${BACKEND_DOCKER_URL}/foods`);
      setFoods(data);
      setFetchError(null);
    } catch (err: any) {
      setFetchError(err.message);
    }
  };
  


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
      </header>
      <>
        <section style={{ marginBottom: '10px' }}>
            <button onClick={() => getJwt()}>Get JWT</button>
            {jwt && (
              <pre>
                <code>{jwt}</code>
              </pre>
            )}
          </section>
          <section>
            <button onClick={() => getFoods()}>
              Get Foods
            </button>
            <ul>
              {foods.map((food, i) => (
                <li>{food.description}</li>
              ))}
            </ul>
            {fetchError && (
              <p style={{ color: 'red' }}>{fetchError}</p>
            )}
        </section>
      </>
    </div>
  );
}

export default App;
