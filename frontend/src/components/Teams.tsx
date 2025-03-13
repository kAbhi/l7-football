import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const navigate = useNavigate();

  const fetchTeams = async () => {
    const res = await axios.get("http://localhost:5000/teams");
    setTeams(res.data);
  };

  return (
    <div className="container">
      <h2>Teams</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      <div className="button-group">
          <button className="primary-button" onClick={fetchTeams}>Get Teams</button>
      </div>
    </div>
  );
};

export default Teams;
