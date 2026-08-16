import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function SupportRoute({ children }) {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (user?.role !== "support" && user?.role !== "admin") {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}
