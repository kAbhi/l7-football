import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Areas = () => {
  const [areas, setAreas] = useState([]);
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
    </div>
  );
};

export default Areas;
