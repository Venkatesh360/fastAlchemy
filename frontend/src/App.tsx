import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Signin from "./pages/Signin";
import Signup from "./pages/Signup";
import PrivateRoute from "./components/PrivateRoutes";


export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/"
        element={
          <PrivateRoute>
            <Dashboard/>
          </PrivateRoute>
        } />
        <Route path="/signin" element={<Signin/>}/>
        <Route path="/signup" element={<Signup/>}/>
      </Routes>
    </Router>
  )
}
