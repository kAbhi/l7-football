import { Link } from "react-router-dom";

const Home = () => (
  <div className="container">
    <h1>Welcome to L7 Football</h1>
    <div className="button-group">
        <Link to="/matches"><button className="primary-button">Matches</button></Link>
        <Link to="/teams"><button className="primary-button">Teams</button></Link>
        <Link to="/players"><button className="primary-button">Players</button></Link>
        <Link to="/areas"><button className="primary-button">Areas</button></Link>
        <a href="http://localhost:5000/apidocs/" target="_blank" rel="noopener noreferrer">
          <button className="api-docs-button">API Docs</button>
        </a>
    </div>
  </div>
);

export default Home;
