'use client';

import { registerUser } from "@/endpoints/auth";
import { RegistrationForm } from "@/types/auth";
import { useMutation } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { SubmitHandler, useForm } from "react-hook-form";
import { FaUser } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import { RiLockPasswordFill } from "react-icons/ri";

const RegistrationModal: React.FC = () => {

    const router = useRouter();

    // FORM SETTINGS
    const { register, handleSubmit, watch, formState: { errors } } = useForm<RegistrationForm>({
        mode: 'onChange'
    });
    const passwordValue = watch('password');

    // TANSTACK
    const { mutate, isPending, isSuccess, error } = useMutation({
        mutationFn: registerUser,
        onSuccess: () => {
            router.push('/dashboard');
        },
        onError: (err: any) => {
            alert(err);
        }
    })

    const onSubmit: SubmitHandler<RegistrationForm> = (data) => {
        mutate(data);
        alert('Done!')
    }

    return (
        <form className="centered-display !justify-between min-h-[80svh] auth-modal bg-surface-card glow-pulse" onSubmit={handleSubmit(onSubmit)}>
            {/* HEADER */}
            <div className="w-full">
                <label className="subheader self-start">Registration</label>
                <hr className="bg-primary-accent w-full h-1" />
            </div>

            {/* MAIN */}
            <div className="w-full centered-display gap-4 mt-8">
                {/* USERNAME */}
                <span className="w-full flex flex-col justify-center align-middle items-center">
                    <div className="w-full flex flex-row justify-center align-middle items-center gap-4">
                        <input id='username' className={`input ${errors.username ? 'input-error' : ''}`} type="text" placeholder="Username" autoComplete="username" {...register('username', {
                            required: 'Username is required.',
                            minLength: { value: 3, message: 'At least 3 characters.' },
                            maxLength: { value: 255, message: 'Max 255 characters.' },
                            pattern: { value: /^\S+$/, message: 'No spaces allowed.' }
                        })} />
                        <FaUser className="text-secondary-accent text-3xl" />
                    </div>
                    {errors.username && (
                        <p className="text-warning mt-1 self-start">{errors.username.message}</p>
                    )}
                </span>

                {/* EMAIL */}
                <span className="w-full flex flex-col justify-center align-middle items-center">
                    <div className="w-full flex flex-row justify-center align-middle items-center gap-4">
                        <input id='email' autoComplete="email" inputMode="email" className={`input ${errors.email ? 'input-error' : ''}`} type="email" placeholder="Email" {...register('email', {
                            required: 'Email is required.',
                            pattern: {
                                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                                message: 'Please enter a valid email address.',
                            },
                            maxLength: { value: 254, message: 'Max 254 characters.' },
                        })} />
                        <MdEmail className="text-secondary-accent text-4xl" />
                    </div>
                    {errors.email && (
                        <p className="text-warning mt-1 self-start">{errors.email.message}</p>
                    )}
                </span>

                {/* PASSWORD */}
                <span className="w-full flex flex-col justify-center align-middle items-center">
                    <div className="w-full flex flex-row justify-center align-middle items-center gap-4">
                        <input id="password" autoComplete="new-password" className={`input ${errors.password ? 'input-error' : ''}`} type='password' placeholder="Password" {...register('password', {
                            required: 'Password is required.',
                            minLength: { value: 8, message: 'At least 8 characters.' },
                            maxLength: { value: 128, message: 'Max 128 characters.' },
                            pattern: {
                                value: /^(?=.*[A-Za-z])(?=.*\d).{8,}$/,
                                message: 'Min 8 chars, include letters and numbers.',
                            },
                        })} />
                        <RiLockPasswordFill className="text-secondary-accent text-4xl" />
                    </div>
                    {errors.password && (
                        <p className="text-warning mt-1 self-start">{errors.password.message}</p>
                    )}
                </span>

                {/* PASSWORD 2 */}
                <span className="w-full flex flex-col justify-center align-middle items-center">
                    <div className="w-full flex flex-row justify-center align-middle items-center gap-4">
                        <input id="password2" autoComplete="new-password" className={`input ${errors.password2 ? 'input-error' : ''}`} type='password' placeholder="Repeat password" {...register('password2', {
                            required: 'Repeating your password is required.',
                            validate: (value) =>
                                value === passwordValue || 'Passwords do not match.'
                        })} />
                        <RiLockPasswordFill className="text-secondary-accent text-4xl" />
                    </div>
                    {errors.password2 && (
                        <p className="text-warning mt-1 self-start">{errors.password2.message}</p>
                    )}
                </span>
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