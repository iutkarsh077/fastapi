import { Link } from "react-router-dom";

const Navbar = () => {
    const navLinks = [
        { name: 'Home', href: '/' },
        { name: 'About', href: '/about' },
        { name: 'Contact', href: '/contact' },
    ];

    return (
        <header className="flex items-center h-20 justify-between px-10 py-4 w-full bg-black border-b border-white/10 backdrop-blur-md">
            <Link to="/" className="flex items-center gap-3 group">
                <span className="w-9 h-9 bg-white rounded-lg flex items-center justify-center text-black font-bold text-lg">
                    🤖
                </span>
                <span className="text-2xl font-bold text-white">
                    ChatBot
                </span>
            </Link>

            <nav className="flex items-center">
                <ul className="flex items-center gap-x-7">
                    {navLinks.map((link) => (
                        <li key={link.name}>
                            <Link to={link.href} className="px-5 py-2.5 text-gray-300 hover:text-white">
                                {link.name}
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>
        </header>

    );
};

export default Navbar;