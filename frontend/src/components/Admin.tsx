import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AddMatchForm from "./AddMatchForm";
import AddTeamForm from "./AddTeamForm";
import AddPlayerForm from "./AddPlayerForm";

const Admin = () => {
  const [activeTab, setActiveTab] = useState("matches");
  const navigate = useNavigate();

  return (
    <div className="container">
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      <h2>Admin Panel</h2>
      <div className="tab-menu">
        <button className={activeTab === "matches" ? "active" : "primary-button"} onClick={() => setActiveTab("matches")}>Add Match</button>
        <button className={activeTab === "teams" ? "active" : "primary-button"} onClick={() => setActiveTab("teams")}>Add Team</button>
        <button className={activeTab === "players" ? "active" : "primary-button"} onClick={() => setActiveTab("players")}>Add Player</button>
      </div>

      <div className="form-section">
        {activeTab === "matches" && <AddMatchForm />}
        {activeTab === "teams" && <AddTeamForm />}
        {activeTab === "players" && <AddPlayerForm />}
      </div>
    </div>
  );
};

export default Admin;
