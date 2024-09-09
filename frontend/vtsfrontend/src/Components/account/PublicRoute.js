import { Navigate } from 'react-router-dom';

const PublicRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('Token'); // Example check for authentication

  return isAuthenticated ? <Navigate to="/over" /> : children;
};


export default PublicRoute;