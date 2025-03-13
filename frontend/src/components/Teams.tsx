import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const res = await axios.get("http://localhost:5000/teams");
        setTeams(res.data);
      } catch (error) {
        console.error("Error fetching teams:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  return (
    <div className="container">
      <h2>Teams</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      {loading ? (
        <p>Loading teams...</p>
      ) : teams.length > 0 ? (
        <div className="cards">
          {teams.map((team) => (
            <div key={team.id} className="card">
              <h3>{team.name}</h3>
              <p><strong>Country:</strong> {team.country}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No teams found.</p>
      )}
    </div>
  );
};

export default Teams;
