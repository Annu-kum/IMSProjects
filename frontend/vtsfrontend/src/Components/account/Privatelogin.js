import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('Token'); // Example check for authentication

  return isAuthenticated ? children : <Navigate to="/" />;
};

export default PrivateRoute;