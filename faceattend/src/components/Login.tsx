import React, { useState } from 'react';
import { Camera, Lock, Mail, Building2, ArrowRight } from 'lucide-react';

interface LoginProps {
  onLogin: () => void;
  darkMode: boolean;
}

function Login({ onLogin, darkMode }: LoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [collegeName, setCollegeName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Mock login/signup - in real app, validate credentials
    onLogin();
  };

  return (
    <div className={`min-h-screen flex items-center justify-center bg-gradient-to-br ${darkMode ? 'from-gray-900 to-gray-800' : 'from-blue-50 to-white'}`}>
      <div className={`max-w-md w-full space-y-8 p-10 rounded-xl shadow-2xl ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
        <div className="text-center space-y-6">
          <div className="flex justify-center">
            <div className={`p-4 rounded-full ${darkMode ? 'bg-blue-900/20' : 'bg-blue-50'}`}>
              <Camera className={`h-12 w-12 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
            </div>
          </div>
          <div>
            <h2 className={`text-3xl font-extrabold tracking-tight ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              {isSignUp ? 'Register Your College' : 'Welcome Back'}
            </h2>
            <p className={`mt-2 text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              {isSignUp ? 'Create your FaceAttend account' : 'Sign in to your attendance system'}
            </p>
          </div>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm space-y-4">
            {isSignUp && (
              <div>
                <label htmlFor="college-name" className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                  College Name
                </label>
                <div className="mt-1 relative">
                  <Building2 className={`absolute left-3 top-3 h-5 w-5 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
                  <input
                    id="college-name"
                    type="text"
                    required={isSignUp}
                    value={collegeName}
                    onChange={(e) => setCollegeName(e.target.value)}
                    className={`appearance-none rounded-lg relative block w-full px-10 py-3 border ${
                      darkMode
                        ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400'
                        : 'border-gray-300 placeholder-gray-500'
                    } focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                    placeholder="Enter your college name"
                  />
                </div>
              </div>
            )}

            <div>
              <label htmlFor="email" className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Email Address
              </label>
              <div className="mt-1 relative">
                <Mail className={`absolute left-3 top-3 h-5 w-5 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className={`appearance-none rounded-lg relative block w-full px-10 py-3 border ${
                    darkMode
                      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400'
                      : 'border-gray-300 placeholder-gray-500'
                  } focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Password
              </label>
              <div className="mt-1 relative">
                <Lock className={`absolute left-3 top-3 h-5 w-5 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
                <input
                  id="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={`appearance-none rounded-lg relative block w-full px-10 py-3 border ${
                    darkMode
                      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400'
                      : 'border-gray-300 placeholder-gray-500'
                  } focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Enter your password"
                />
              </div>
            </div>
          </div>

          {!isSignUp && (
            <div className="flex items-center justify-end">
              <button
                type="button"
                className={`text-sm font-medium ${
                  darkMode ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-500'
                }`}
              >
                Forgot your password?
              </button>
            </div>
          )}

          <div>
            <button
              type="submit"
              className={`group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white ${
                darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'
              } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200`}
            >
              <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                <ArrowRight className={`h-5 w-5 ${darkMode ? 'text-blue-400' : 'text-blue-300'} group-hover:text-blue-200`} />
              </span>
              {isSignUp ? 'Create Account' : 'Sign In'}
            </button>
          </div>

          <div className="text-center">
            <button
              type="button"
              onClick={() => setIsSignUp(!isSignUp)}
              className={`text-sm font-medium ${darkMode ? 'text-gray-400 hover:text-gray-300' : 'text-gray-600 hover:text-gray-500'}`}
            >
              {isSignUp ? 'Already have an account? Sign in' : 'New here? Create an account'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;