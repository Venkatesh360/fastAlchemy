import React, { useState } from 'react'
import axios from 'axios'


function Signup() {
    const [username, setUsername] = useState<string>("")
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")

    const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const user = await axios.post('http://127.0.0.1:8000/api/auth/signup', {
            username: username,
            email: email,
            password: password
        })

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