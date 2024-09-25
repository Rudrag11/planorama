
import "./login.css"; // Ensure you import your CSS file

const Signup = () => {

  return (
    <div className="login-main">
      <form class="form">
            <p class="form-title">Create Account</p>
            <div class="input-container">
              <input placeholder="Enter Name" type="text" />
              <input placeholder="Enter Phone number" type="text" />
              <input placeholder="Enter email" type="email" />
            </div>
            <div class="input-container">
              <input placeholder="Create password" type="password" />
            </div>
            <button class="submit" type="submit">
              Sign in
            </button>

            <p class="signup-link">
              Have an account?
              <a href="Login">Login</a>
            </p>
          </form>
    </div>
  );
};

export default Signup;
