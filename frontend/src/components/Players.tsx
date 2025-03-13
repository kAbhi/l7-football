import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Players = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const navigate = useNavigate();

  // Fetch teams for dropdown on page load
  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const res = await axios.get("http://localhost:5000/teams");
        setTeams(res.data);
      } catch (error) {
        console.error("Error fetching teams:", error);
      }
    };

    fetchTeams();
  }, []);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        let url = "http://localhost:5000/players";
        if (selectedTeam) {
          url += `?team=${encodeURIComponent(selectedTeam)}`;
        }

        const res = await axios.get(url);
        setPlayers(res.data);
      } catch (error) {
        console.error("Error fetching players:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayers();
  }, [selectedTeam]);

  return (
    <div className="container">
      <h2>Players</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>

      {/* Filters */}
      <div className="filters">
        <select value={selectedTeam} onChange={(e) => setSelectedTeam(e.target.value)}>
          <option value="">All Teams</option>
          {teams.map((team) => (
            <option key={team.id} value={team.name}>{team.name}</option>
          ))}
        </select>
      </div>

      {/* Data cards */}
      {loading ? (
        <p>Loading players...</p>
      ) : players.length > 0 ? (
        <div className="cards">
          {players.map((player) => (
            <div key={player.id} className="card">
              <h3>{player.name}</h3>
              <p><strong>Team:</strong> {player.team}</p>
              <p><strong>Position:</strong> {player.position}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No players found.</p>
      )}
    </div>
  );
};

export default Players;
