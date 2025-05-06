import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { jwtDecode } from 'jwt-decode'

type User = {
    username: string
};

type AuthContextType = {
    user: User | null;
    token: String | null;
    isLoggedIn: boolean;
    login: (userData: User, token: string) => void;
    logout: () => void;
    loading: boolean;
}

type AuthProviderProps = {
    children: ReactNode
}

type DecodedToken = {
    exp: number;
    [key: string]: any;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
    const context = useContext(AuthContext)

    if (!context) {
        throw new Error("useAuth must be used within a AuthProvider")
    }

    return context
}


export function AuthProvider({ children }: AuthProviderProps) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<String | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const storedUser = localStorage.getItem('user')
        const storedToken = localStorage.getItem('token')

        if (storedToken) {
            try {
                const decoded: DecodedToken = jwtDecode(storedToken)
                const isExpired: boolean = decoded.exp * 1000 < Date.now()

                if (isExpired) {
                    localStorage.removeItem('user')
                    localStorage.removeItem('token')

                    setUser(null)
                    setToken(null)
                    return;
                } else {
                    setToken(storedToken);
                    if (storedUser) { setUser(JSON.parse(storedUser)) }
                }
            } catch (error) {
                console.error('Invalid token')
                setUser(null)
                setToken(null)
            }
        }
        setLoading(false)
    }, []);


    const login = (userData: User, token: string) => {
        localStorage.setItem("user", JSON.stringify(userData));
        localStorage.setItem("token", token);
        setUser(userData);
        setToken(token);
    }

    const logout = () => {
        localStorage.removeItem('user')
        localStorage.removeItem('token')
        setUser(null)
        setToken(null)
    }

    const isLoggedIn = !!user

    return (
        <AuthContext.Provider value={{ user, token, isLoggedIn, login, logout, loading }}>
        {children}
        </AuthContext.Provider>
    )
};




