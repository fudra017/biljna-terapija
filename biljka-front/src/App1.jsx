// App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Analiza from './pages/Analiza';
import Login from './pages/Login';
import Contact from './pages/Contact';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="ml-64 w-full">
          {/* Testni Tailwind kvadrat u donjoj desnoj četvrtini ekrana */}
	  <div className="fixed bottom-0 right-0 w-1/4 h-1/4 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 text-white flex items-center justify-center text-xl font-bold shadow-xl rounded-tl-2xl">
  	    Tailwind Test
	  </div>      
	  <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analiza" element={<Analiza />} />
            <Route path="/login" element={<Login />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;