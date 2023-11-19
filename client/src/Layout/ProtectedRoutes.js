import { useEffect, useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";



export default function ProtectedRoutes() {
  const [isAuth, setIsAuth] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in by checking the presence of a token in local storage
    console.log(localStorage.getItem("userToken"))
    const token = localStorage.getItem("userToken");
    if (token) {
      setIsAuth(true);
    } else {
      navigate("/login");
    }
  }, [navigate]);

  return <>{isAuth && <Outlet />}</>;
}
