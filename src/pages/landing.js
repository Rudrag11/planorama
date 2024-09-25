import './landing.css'
import image from './landing pic.png'
import{useNavigate} from 'react-router-dom'

const Landing=()=>{
    const navigate=useNavigate();
    return(
        <div className='main'>
            <div className='header'>
                <h2>PLANORAMA</h2>
            </div>
            <div className='landingbody'>
                <p>Map Your Adventure,</p>
                <p>Seamlessly!</p>
                <img src={image} alt="logo"/>
                <div className="Options">
                    <button className='Get-started' onClick={()=> navigate('signup')}>Get Started</button>
                    <button className="Login-btn" onClick={()=> navigate('login')}>Login</button>
                </div>
            </div>
        </div>
    )
};
export default Landing;