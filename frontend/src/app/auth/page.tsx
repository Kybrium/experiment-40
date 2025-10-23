import LoginModal from "@/components/auth/LoginModal";
import RegistrationModal from "@/components/auth/RegistrationModal";
import StarsBg from "@/components/bg/StarsBg";

export default function Auth() {
    return (
        <main className="min-h-screen centered-display py-8">
            <StarsBg />
            <RegistrationModal />
            <LoginModal />
        </main>
    );
}
