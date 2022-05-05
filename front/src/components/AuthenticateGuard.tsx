/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable react/function-component-definition */
import { ReactNode } from 'react';
import { Redirect, useLocation } from 'react-router-dom';

interface dummyProps {
  children:ReactNode
}


function AuthenticatedGuard(props: dummyProps) {
  const { children } = props;
  const isAuthenticated  = true;
  const location = useLocation();

  return isAuthenticated ? <div>{ children }</div> : <Redirect to={{
    pathname: '/login',
    state: { from: location },
  }} />;
};

export default AuthenticatedGuard;
