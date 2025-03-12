import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import AddMatchForm from "./AddMatchForm";

const Matches = () => {
  const [matches, setMatches] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const navigate = useNavigate();

  const fetchMatches = async () => {
    const res = await axios.get("http://localhost:5000/matches");
    setMatches(res.data);
  };

  return (
    <div className="container">
      <h2>Matches</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      <div className="button-group">
          <button className="primary-button" onClick={fetchMatches}>Get Matches</button>
          <button className="primary-button" onClick={() => setShowForm(!showForm)}>Add Match</button>
      </div>
      {showForm && <AddMatchForm onMatchAdded={fetchMatches} />}
      <ul>
        {matches.map((match) => (
          <li key={match.id}>{match.team1} vs {match.team2} on {match.date} ({match.location})</li>
        ))}
      </ul>
    </div>
  );
};

export default Matches;
