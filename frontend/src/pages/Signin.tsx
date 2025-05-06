import React, { useState} from 'react'
import axios from 'axios'
import { useAuth } from '../context/UserContext'
import { useNavigate } from 'react-router-dom'

function Signup() {
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const {login} = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const res = await axios.post('http://127.0.0.1:8000/api/auth/signin', {
            email: email,
            password: password
        })
        console.log(res)
        if (res.status == 200){
            login({username:res.data.user.username}, res.data.access_token)
            navigate("/")
        }
        
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
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