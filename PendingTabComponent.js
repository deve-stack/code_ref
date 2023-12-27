import React from "react";
import moment from "moment";
import DummyImage from "../../../Assets/noimg.jpg";
import IndivualStatus from "./IndivualStatus";
import { useSelector } from "react-redux";

const PendingTabComponent = ({ data }) => {
  const loader = useSelector((state) => state.Loading.loading);
  return (
    <section className="review">
      <div className="container">
        <div className="row py-3">
          {data.map((item) => {
            if (item.status != "Pending") return null;
            return <IndivualStatus data={item} />;
          })}

          {!data.some((item) => item.status == "Pending") && !loader ? (
            <>
              <div className="row  ">
                <div className="col-md-12  text-center">
                  <p className="text-danger">No data found for pending status</p>
                </div>
              </div>
            </>
          ) : null}
        </div>
      </div>
    </section>
  );
};

export default PendingTabComponent;
