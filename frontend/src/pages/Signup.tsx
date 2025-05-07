import React, { useState } from 'react'
import axios from 'axios'
import { useAuth } from '../context/UserContext'
import { useNavigate } from 'react-router-dom'
import "./Signup.css"

function Signup() {
    const [username, setUsername] = useState<string>("")
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const {login} = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const user = await axios.post('http://127.0.0.1:8000/api/auth/signup', {
            username: username,
            email: email,
            password: password
        })
        if (user.status == 200){
            login({username:user.data.user.username}, user.data.access_token)
            navigate("/")
        }

        console.log(user)
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="">
                    <input type="text" placeholder='username' value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div className="">
                    <input type="email" placeholder='email' value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div className="">
                    <input type="password" placeholder='password' value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type='submit'>Submit</button>
            </form>
        </div>
    )
}

export default Signup