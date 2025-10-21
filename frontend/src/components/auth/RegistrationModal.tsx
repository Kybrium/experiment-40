'use client';

import Link from "next/link";
import { useState } from "react";
import { FaUser } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import { RiLockPasswordFill } from "react-icons/ri";

const RegistrationModal: React.FC = () => {

    // STATES
    const [username, setUsername] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [password2, setPassword2] = useState<string>('');

    return (
        <form className="centered-display auth-modal bg-surface-card glow-pulse">
            {/* HEADER */}
            <label className="subheader self-start">Registration</label>
            <hr className="bg-primary-accent w-full h-1" />

            {/* MAIN */}
            <div className="w-full centered-display gap-4 mt-8">
                <span className="w-full flex flex-row justify-center align-middle items-center gap-4">
                    <input className="input" type="text" placeholder="username" onChange={(e) => setUsername(e.target.value)} />
                    <FaUser className="text-secondary-accent text-3xl" />
                </span>
                <span className="w-full flex flex-row justify-center align-middle items-center gap-4">
                    <input className="input" type="email" placeholder="email" onChange={(e) => setEmail(e.target.value)} />
                    <MdEmail className="text-secondary-accent text-4xl" />
                </span>
                <span className="w-full flex flex-row justify-center align-middle items-center gap-4">
                    <input className="input" type='password' placeholder="password" onChange={(e) => setPassword(e.target.value)} />
                    <RiLockPasswordFill className="text-secondary-accent text-4xl" />
                </span>
                <span className="w-full flex flex-row justify-center align-middle items-center gap-4">
                    <input className="input" type='password' placeholder="repeat password" onChange={(e) => setPassword2(e.target.value)} />
                    <RiLockPasswordFill className="text-secondary-accent text-4xl" />
                </span>
                <p className="text-warning">All fields are required</p>
            </div>

            {/* FOOTER */}
            <div className="centered-row-display centered-display mt-8 gap-3">
                <button className="btn btn-primary w-full cursor-pointer" type="submit">Register</button>
                <Link href='' className="btn btn-secondary w-full">Back to Login</Link>
            </div>
        </form>
    )
}

export default RegistrationModal;