import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import AddTeamForm from "./AddTeamForm";

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [showForm, setShowForm] = useState(false);
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
          <button className="primary-button" onClick={() => setShowForm(!showForm)}>Add Team</button>
      </div>
      {showForm && <AddTeamForm onTeamAdded={fetchTeams} />}
      <ul>{teams.map((t) => <li key={t.id}>{t.name} ({t.country})</li>)}</ul>
    </div>
  );
};

export default Teams;
