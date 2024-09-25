import "./login.css"; // Ensure you import your CSS file

const Login = () => {
  return (
    <div className="login-main">
          <form class="form">
            <p class="form-title">Welcome Back!</p>
            <div class="input-container">
              <input placeholder="Enter email" type="email" />
            </div>
            <div class="input-container">
              <input placeholder="Enter password" type="password" />
            </div>
            <button class="submit" type="submit">
              Login
            </button>

            <p class="signup-link">
              No account?
              <a href="Signup">Sign up</a>
            </p>
          </form>
        </div>
  );
};

export default Login;
