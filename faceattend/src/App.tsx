import React, { useState } from 'react';
import { Camera, UserPlus, Users, UserMinus, UserCog, FileSpreadsheet, Moon, Sun, Search, LogOut } from 'lucide-react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import AddStudent from './components/AddStudent';
import ModifyStudent from './components/ModifyStudent';
import DeleteStudent from './components/DeleteStudent';
import ScanAttendance from './components/ScanAttendance';
import Reports from './components/Reports';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard');

  if (!isLoggedIn) {
    return <Login onLogin={() => setIsLoggedIn(true)} darkMode={darkMode} />;
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'add':
        return <AddStudent />;
      case 'modify':
        return <ModifyStudent />;
      case 'delete':
        return <DeleteStudent />;
      case 'scan':
        return <ScanAttendance />;
      case 'reports':
        return <Reports />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      <nav className={`fixed top-0 left-0 right-0 ${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg z-50`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className={`flex-shrink-0 flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                <Camera className="h-8 w-8 mr-2" />
                <span className="text-xl font-bold">FaceAttend</span>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <NavButton icon={<Users />} text="Dashboard" onClick={() => setCurrentPage('dashboard')} active={currentPage === 'dashboard'} darkMode={darkMode} />
                <NavButton icon={<UserPlus />} text="Add Student" onClick={() => setCurrentPage('add')} active={currentPage === 'add'} darkMode={darkMode} />
                <NavButton icon={<UserCog />} text="Modify" onClick={() => setCurrentPage('modify')} active={currentPage === 'modify'} darkMode={darkMode} />
                <NavButton icon={<UserMinus />} text="Delete" onClick={() => setCurrentPage('delete')} active={currentPage === 'delete'} darkMode={darkMode} />
                <NavButton icon={<Camera />} text="Scan" onClick={() => setCurrentPage('scan')} active={currentPage === 'scan'} darkMode={darkMode} />
                <NavButton icon={<FileSpreadsheet />} text="Reports" onClick={() => setCurrentPage('reports')} active={currentPage === 'reports'} darkMode={darkMode} />
              </div>
            </div>
            <div className="flex items-center">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className={`p-2 rounded-lg ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}
              >
                {darkMode ? <Sun className="h-5 w-5 text-gray-300" /> : <Moon className="h-5 w-5 text-gray-500" />}
              </button>
              <button
                onClick={() => setIsLoggedIn(false)}
                className={`ml-4 p-2 rounded-lg ${darkMode ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-gray-100 text-gray-500'}`}
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-16">
        {renderPage()}
      </main>
    </div>
  );
}

function NavButton({ icon, text, onClick, active, darkMode }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center px-3 py-2 text-sm font-medium ${
        active
          ? darkMode
            ? 'border-blue-500 text-white'
            : 'border-blue-500 text-gray-900'
          : darkMode
          ? 'text-gray-300 hover:text-white'
          : 'text-gray-500 hover:text-gray-700'
      }`}
    >
      {React.cloneElement(icon, { className: 'h-5 w-5 mr-2' })}
      {text}
    </button>
  );
}

export default App;