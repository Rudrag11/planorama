import Landing from './pages/landing.js'
import './App.css';
import {Routes, Route} from 'react-router-dom'
import Login from './pages/login/login.js'
import Signup from './pages/login/signup.js'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </div>
  );
}

export default App;
