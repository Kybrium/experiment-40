'use client';

import { fetchCurrentUser, registerUser } from "@/endpoints/auth";
import { RegistrationForm } from "@/types/auth";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { SubmitHandler, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { FaUser } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import { RiLockPasswordFill } from "react-icons/ri";
import { toast } from "react-toastify";

const RegistrationModal: React.FC<{ setIsLogin: (v: boolean) => void }> = ({ setIsLogin }) => {

    const router = useRouter();
    const queryClient = useQueryClient();
    const { t } = useTranslation('translation', { keyPrefix: 'Auth.Registration' });

    // FORM SETTINGS
    const { register, handleSubmit, watch, formState: { errors } } = useForm<RegistrationForm>({
        mode: 'onChange'
    });
    const passwordValue = watch('password');

    // TANSTACK
    const { mutate, isPending, isSuccess, error } = useMutation({
        mutationFn: registerUser,
        onSuccess: async () => {
            toast.success(t('toast_success'));
            await queryClient.invalidateQueries({ queryKey: ["me"] });
            await queryClient.prefetchQuery({ queryKey: ["me"], queryFn: fetchCurrentUser });
            setTimeout(() => router.push('/dashboard'), 1200);
        },
        onError: (err: unknown) => {
            const msg = err instanceof Error ? err.message : t('toast_error_fallback');
            toast.error(msg ?? t('toast_error_fallback'));
        },
    })

    const onSubmit: SubmitHandler<RegistrationForm> = (data) => {
        mutate(data);
    }

    return (
        <form className="centered-display !justify-between min-h-[80svh] auth-modal bg-surface-card/70 glow-pulse" onSubmit={handleSubmit(onSubmit)}>
            {/* HEADER */}
            <div className="w-full">
                <label className="subheader self-start">{t('title')}</label>
                <hr className="bg-primary-accent w-full h-1" />
            </div>

            {/* MAIN */}
            <div className="w-full centered-display gap-4 mt-8">
                {/* USERNAME */}
                <span className="w-full flex flex-col justify-center align-middle items-center">
                    <div className="w-full flex flex-row justify-center align-middle items-center gap-4">
                        <input id='username' className={`input ${errors.username ? 'input-error' : ''}`} type="text" placeholder={t('username_placeholder')} autoComplete="username" {...register('username', {
                            required: t('username_required'),
                            minLength: { value: 3, message: t('username_min') },
                            maxLength: { value: 255, message: t('username_max') },
                            pattern: { value: /^\S+$/, message: t('username_no_spaces') }
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
                        <input id='email' autoComplete="email" inputMode="email" className={`input ${errors.email ? 'input-error' : ''}`} type="email" placeholder={t('email_placeholder')} {...register('email', {
                            required: t('email_required'),
                            pattern: {
                                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                                message: t('email_pattern'),
                            },
                            maxLength: { value: 254, message: t('email_max') },
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
                        <input id="password" autoComplete="new-password" className={`input ${errors.password ? 'input-error' : ''}`} type='password' placeholder={t('password_placeholder')} {...register('password', {
                            required: t('password_required'),
                            minLength: { value: 8, message: t('password_min') },
                            maxLength: { value: 128, message: t('password_max') },
                            pattern: {
                                value: /^(?=.*[A-Za-z])(?=.*\d).{8,}$/,
                                message: t('password_complexity'),
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
                        <input id="password2" autoComplete="new-password" className={`input ${errors.password2 ? 'input-error' : ''}`} type='password' placeholder={t('password2_placeholder')} {...register('password2', {
                            required: t('password2_required'),
                            validate: (value) =>
                                value === passwordValue || t('password2_match')
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
                <button className="btn btn-primary w-full cursor-pointer" type="submit">{t('button_submit')}</button>
                <button onClick={() => setIsLogin(true)} className="btn btn-secondary w-full cursor-pointer" type="reset">{t('button_back_to_login')}</button>
            </div>
        </form>
    )
}

export default RegistrationModal;