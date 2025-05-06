import { Navigate } from "react-router-dom"
import { useAuth } from "../context/UserContext"


type PrivateRouteProps = {
    children: JSX.Element;
}

const PrivateRoute = ({ children }: any) => {
    const { isLoggedIn, loading } = useAuth()

    if (loading) {
        return <div className="">Loading...</div>
    }

    return isLoggedIn ? children : <Navigate to="/signin" replace/>
}

export default PrivateRoute;