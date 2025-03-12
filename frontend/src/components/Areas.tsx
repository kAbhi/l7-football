import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import AddAreaForm from "./AddAreaForm";

const Areas = () => {
  const [areas, setAreas] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const navigate = useNavigate();

  const fetchAreas = async () => {
    const res = await axios.get("http://localhost:5000/areas");
    setAreas(res.data);
  };

  return (
    <div className="container">
      <h2>Areas</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      <div className="button-group">
          <button className="primary-button" onClick={fetchAreas}>Get Areas</button>
      </div>
      <ul>{areas.map((a) => <li key={a.id}>{a.city}, {a.country}</li>)}</ul>
    </div>
  );
};

export default Areas;
