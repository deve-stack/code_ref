import React, { useState } from "react";

import OngoingStaus from "./OngoingStaus";
import ConfirmationPopup from "../../../Components/Body/Venues/Bids/Popup";
import { useDispatch, useSelector } from "react-redux";
import { Toaster, toast } from "react-hot-toast";
import {
  AcceptGigActionByArtistManager,
  AcceptGigActionByVeneuManger,
  RejectGigActionByArtistManager,
  RejectGigActionByVenueManger,
} from "../../../Redux/Action/Bidding";

const OnGointTabComponent = ({ data, callMyBidsAction }) => {
  const dispatch = useDispatch();
  const [showConfirmationPopup, setShowConfirmationPopup] = useState(false);
  const [selectedBid, setSelectedBid] = useState(null);
  const Profile = useSelector((state) => state.Auth.profile);
  const authToken = useSelector((state) => state.Auth.authToken);
  const loader = useSelector((state) => state.Loading.loading);

  //Confirmation Popup
  const openConfirmationPopup = (bidId, venue, artist, type) => {
    setSelectedBid({ bidId, type, venue, artist });
    setShowConfirmationPopup(true);
  };
  const closeConfirmationPopup = () => {
    if (selectedBid.type == "Accept" && Profile.venue_owner == true) {
      dispatch(
        AcceptGigActionByVeneuManger(
          selectedBid,
          authToken,
          (type, message) => {
            toast[type](`${message}`, {
              duration: 5000,
            });
            callMyBidsAction();
          }
        )
      );
    }

    if (selectedBid.type == "Accept" && Profile.artist_or_band == true) {
      dispatch(
        AcceptGigActionByArtistManager(
          selectedBid,
          authToken,
          (type, message) => {
            toast[type](`${message}`, {
              duration: 5000,
            });
            callMyBidsAction();
          }
        )
      );
    }

    if (selectedBid.type == "Reject" && Profile.venue_owner == true) {
      dispatch(
        RejectGigActionByVenueManger(
          selectedBid,
          authToken,
          (type, message) => {
            toast[type](`${message}`, {
              duration: 5000,
            });
            callMyBidsAction();
          }
        )
      );
    }

    if (selectedBid.type == "Reject" && Profile.artist_or_band == true) {
      dispatch(
        RejectGigActionByArtistManager(
          selectedBid,
          authToken,
          (type, message) => {
            toast[type](`${message}`, {
              duration: 5000,
            });
            callMyBidsAction();
          }
        )
      );
    }
    setShowConfirmationPopup(false);
    setSelectedBid({});
  };
  const cancelConfiramtionPopup = () => {
    setShowConfirmationPopup(false);
    setSelectedBid({});
  };

  return (
    <>
      <section className="review">
        <div className="container">
          <div className="row py-3">
            {data.map((item) => {
              if (item.status != "Ongoing") return null;
              return (
                <OngoingStaus
                  openConfirmationPopup={openConfirmationPopup}
                  data={item}
                />
              );
            })}

            {!data.some((item) => item.status == "Ongoing") && !loader ? (
              <>
                <div className="row">
                  <div className="col-md-12  text-center">
                    <p className="text-danger">No data found for ongoing status</p>
                  </div>
                </div>
              </>
            ) : null}
          </div>
        </div>
      </section>
      <ConfirmationPopup
        cancel={cancelConfiramtionPopup}
        showModal={showConfirmationPopup}
        closeModal={closeConfirmationPopup}
        selectedBid={selectedBid}
      />
      <Toaster />
    </>
  );
};

export default OnGointTabComponent;
