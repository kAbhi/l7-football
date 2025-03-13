import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Matches = () => {
  const [matches, setMatches] = useState([]);
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [selectedMonth, setSelectedMonth] = useState("");
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

  // Fetch matches on page load
  useEffect(() => {
    const fetchMatches = async () => {
      try {
        let url = "http://localhost:5000/matches";
        let params = [];

        if (selectedTeam) params.push(`team=${encodeURIComponent(selectedTeam)}`);
        if (selectedMonth) params.push(`month=${selectedMonth}`);

        if (params.length > 0) {
          url += `?${params.join("&")}`;
        }

        const res = await axios.get(url);
        setMatches(res.data);
      } catch (error) {
        console.error("Error fetching matches:", error);
      }
    };
    fetchMatches();
  }, [selectedTeam, selectedMonth]);

  // Generate months list for current year
  const getMonths = () => {
    const currentYear = new Date().getFullYear();
    return [...Array(12)].map((_, i) => {
      const month = String(i + 1).padStart(2, "0");
      return `${currentYear}-${month}`;
    });
  };

  return (
    <div className="container">
      <h2>Matches</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>

      {/* Filters */}
      <div className="filters">
        <select value={selectedTeam} onChange={(e) => setSelectedTeam(e.target.value)}>
          <option value="">All Teams</option>
          {teams.map((team) => (
            <option key={team.id} value={team.name}>{team.name}</option>
          ))}
        </select>

        <select value={selectedMonth} onChange={(e) => setSelectedMonth(e.target.value)}>
          <option value="">All Months</option>
          {getMonths().map((month) => (
            <option key={month} value={month}>{month}</option>
          ))}
        </select>
      </div>

      {/* Data cards */}
      <div className="cards">
        {matches.map((match) => (
          <div key={match.id} className="card">
            <h3>{match.team1} vs {match.team2}</h3>
            <p><strong>Date:</strong> {match.date}</p>
            <p><strong>Location:</strong> {match.location}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Matches;
