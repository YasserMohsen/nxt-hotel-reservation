from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import RoomType, Room, Reservation
# from .serializers import RoomTypeSerializer
from apps.users.constants import ADMIN_USER, AGENT_USER, GUEST_USER
# from apps.users.permissions import IsAdminOrReadOnlyPermission

User = get_user_model()

class ViewSetGenericTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        admin_role = Group.objects.create(name=ADMIN_USER)
        self.user_admin = User.objects.create(username="admin-test", email="admin.test@example.com", role=admin_role)
        agent_role = Group.objects.create(name=AGENT_USER)
        self.user_agent = User.objects.create(username="agent-test", email="agent.test@example.com", role=agent_role)
        guest_role = Group.objects.create(name=GUEST_USER)
        self.user_guest = User.objects.create(username="guest-test", email="guest.test@example.com", role=guest_role)
        self.user_guest_2 = User.objects.create(username="guest-test-2", email="guest.test.2@example.com", role=guest_role)


class RoomTypeViewSetTestCase(ViewSetGenericTestCase):
    def setUp(self):
        super().setUp()
        self.room_type = RoomType.objects.create(name="Single Room", description="A single room type", capacity=1, price_per_night=50)

    # LIST
    def test_list_room_types(self):
        url = reverse("room-types-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_room_types_as_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("room-types-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_room_types_as_agent(self):
        self.client.force_authenticate(user=self.user_agent)
        url = reverse("room-types-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_room_types_as_guest(self):
        self.client.force_authenticate(user=self.user_guest)
        url = reverse("room-types-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # RETRIEVE
    def test_retrieve_room_type(self):
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_room_type_as_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_room_type_as_agent(self):
        self.client.force_authenticate(user=self.user_agent)
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_room_type_as_guest(self):
        self.client.force_authenticate(user=self.user_guest)
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # CREATE
    def test_create_room_type(self):
        data = {"name": "Double", "description": "A double room type", "capacity": 2, "price_per_night": 100}
        url = reverse("room-types-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_room_type_as_guest(self):
        self.client.force_authenticate(user=self.user_guest)
        data = {"name": "Double", "description": "A double room type", "capacity": 2, "price_per_night": 100}
        url = reverse("room-types-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_room_type_as_agent(self):
        self.client.force_authenticate(user=self.user_agent)
        data = {"name": "Double", "description": "A double room type", "capacity": 2, "price_per_night": 100}
        url = reverse("room-types-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_room_type_as_admin(self):
        # Ensure only admin users can create room types (POST request)
        self.client.force_authenticate(user=self.user_admin)
        data = {"name": "Double", "description": "A double room type", "capacity": 2, "price_per_night": 100}
        url = reverse("room-types-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # UPDATE

    def test_update_room_type(self):
        data = {"name": "Updated Single", "description": "An updated single room type"}
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_room_type_as_admin(self):
        # Ensure only admin users can update room types (PUT request)
        self.client.force_authenticate(user=self.user_admin)
        data = {"name": "Updated Single", "description": "An updated single room type"}
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room_type.refresh_from_db()
        self.assertEqual(self.room_type.name, "Updated Single")

    def test_update_room_type_as_guest(self):
        # Ensure normal users cannot update room types (PUT request)
        self.client.force_authenticate(user=self.user_guest)
        data = {"name": "Updated Single", "description": "An updated single room type"}
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE
    def test_delete_room_type_as_admin(self):
        # Ensure only admin users can delete room types (DELETE request)
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_room_type_as_guest(self):
        # Ensure normal users cannot delete room types (DELETE request)
        self.client.force_authenticate(user=self.user_guest)
        url = reverse("room-types-detail", args=[self.room_type.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RoomViewSetTestCase(ViewSetGenericTestCase):
    def setUp(self):
        super().setUp()
        self.room_type = RoomType.objects.create(name="Single Room", description="A single room type", capacity=1, price_per_night=50)
        self.room = Room.objects.create(number='A333', room_type=self.room_type)

    # testing only list and retrieve for now, skip the others as they are the same as RoomType

    # LIST
    def test_list_rooms(self):
        url = reverse("rooms-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_rooms_as_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("rooms-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_rooms_as_agent(self):
        self.client.force_authenticate(user=self.user_agent)
        url = reverse("rooms-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_rooms_as_guest(self):
        self.client.force_authenticate(user=self.user_guest)
        url = reverse("rooms-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # RETRIEVE
    def test_retrieve_room(self):
        url = reverse("rooms-detail", args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_room_as_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("rooms-detail", args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_room_as_agent(self):
        self.client.force_authenticate(user=self.user_agent)
        url = reverse("rooms-detail", args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_room_as_guest(self):
        self.client.force_authenticate(user=self.user_guest)
        url = reverse("rooms-detail", args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReservationViewSetsTestCase(ViewSetGenericTestCase):
    def setUp(self):
        super().setUp()
        self.room_type = RoomType.objects.create(name="Single Room", description="A single room type", capacity=1, price_per_night=50)
        self.room = Room.objects.create(number='A333', room_type=self.room_type)
        self.reservation = Reservation.objects.create(
            user=self.user_guest,
            check_in_date="2024-10-10",
            check_out_date="2024-10-15",
            assigned_room=self.room,
        )
        self.reservation_2 = Reservation.objects.create(
            user=self.user_guest,
            check_in_date="2024-12-01",
            check_out_date="2024-12-05",
            assigned_room=self.room,
        )

    # CREATE
    def test_create_reservation(self):
        data = {"user": self.user_guest.id, "check_in_date": "2024-11-01", "check_out_date": "2024-11-10", "selected_room_type": self.room_type.id}
        url = reverse("new-reservation-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reservation_as_guest(self):
        self.client.force_authenticate(user=self.user_guest)
        data = {"user": self.user_guest.id, "check_in_date": "2024-11-01", "check_out_date": "2024-11-10", "selected_room_type": self.room_type.id}
        url = reverse("new-reservation-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reservation_as_guest_date_range_order(self):
        self.client.force_authenticate(user=self.user_guest)
        data = {"user": self.user_guest.id, "check_in_date": "2024-11-10", "check_out_date": "2024-11-01", "selected_room_type": self.room_type.id}
        url = reverse("new-reservation-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_as_guest_date_in_past(self):
        self.client.force_authenticate(user=self.user_guest)
        data_list = [
            {"user": self.user_guest.id, "check_in_date": "2022-11-01", "check_out_date": "2022-11-11", "selected_room_type": self.room_type.id},
            {"user": self.user_guest.id, "check_in_date": "2023-09-22", "check_out_date": "2023-10-20", "selected_room_type": self.room_type.id}
        ]
        for data in data_list:
            url = reverse("new-reservation-list")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_as_guest_does_not_exist_room_type(self):
        self.client.force_authenticate(user=self.user_guest)
        data = {"user": self.user_guest.id, "check_in_date": "2024-11-10", "check_out_date": "2024-11-01", "selected_room_type": 1000}
        url = reverse("new-reservation-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_as_guest_conflict_date(self):
        self.client.force_authenticate(user=self.user_guest)
        data_list = [
            {"user": self.user_guest.id, "check_in_date": "2024-10-10", "check_out_date": "2024-10-15", "selected_room_type": self.room_type.id},
            {"user": self.user_guest.id, "check_in_date": "2024-10-11", "check_out_date": "2024-10-13", "selected_room_type": self.room_type.id},
            {"user": self.user_guest.id, "check_in_date": "2024-10-09", "check_out_date": "2024-10-11", "selected_room_type": self.room_type.id},
            {"user": self.user_guest.id, "check_in_date": "2024-10-08", "check_out_date": "2024-10-17", "selected_room_type": self.room_type.id},
            {"user": self.user_guest.id, "check_in_date": "2024-10-14", "check_out_date": "2024-10-20", "selected_room_type": self.room_type.id}
        ]
        url = reverse("new-reservation-list")
        for data in data_list:
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_as_guest_non_conflict_date(self):
        self.client.force_authenticate(user=self.user_guest)
        data_list = [
            {"user": self.user_guest.id, "check_in_date": "2024-10-15", "check_out_date": "2024-10-20", "selected_room_type": self.room_type.id},
            {"user": self.user_guest.id, "check_in_date": "2024-10-05", "check_out_date": "2024-10-10", "selected_room_type": self.room_type.id},
            {"user": self.user_guest.id, "check_in_date": "2024-10-01", "check_out_date": "2024-10-05", "selected_room_type": self.room_type.id}
        ]
        url = reverse("new-reservation-list")
        for data in data_list:
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    # LIST
    def test_list_reservations_as_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("reservations-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reservations_as_guest(self):
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("reservations-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # RETRIEVE
    def test_list_reservations_as_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        url = reverse("reservations-detail", args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reservations_as_agent(self):
        self.client.force_authenticate(user=self.user_agent)
        url = reverse("reservations-detail", args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reservations_as_guest_owner(self):
        self.client.force_authenticate(user=self.user_guest)
        url = reverse("reservations-detail", args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reservations_as_guest_non_owner(self):
        self.client.force_authenticate(user=self.user_guest_2)
        url = reverse("reservations-detail", args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # UPDATE DATE RANGE
    def test_update_reservation_date_range(self):
        data = {"check_in_date": "2024-10-10", "check_out_date": "2024-10-16"}
        url = reverse("reservation-dates-detail", args=[self.reservation.id])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_reservation_date_range_as_guest(self):
        self.client.force_authenticate(user=self.user_guest)
        data = {"check_in_date": "2024-10-10", "check_out_date": "2024-10-16"}
        url = reverse("reservation-dates-detail", args=[self.reservation.id])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_reservation_date_range_as_agent(self):
        self.client.force_authenticate(user=self.user_agent)
        data = {"check_in_date": "2024-10-10", "check_out_date": "2024-10-16"}
        url = reverse("reservation-dates-detail", args=[self.reservation.id])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertEqual(str(self.reservation.check_in_date), "2024-10-10")

    def test_update_reservation_date_range_as_agent_conflict(self):
        self.client.force_authenticate(user=self.user_agent)
        data = {"check_in_date": "2024-12-02", "check_out_date": "2024-12-10"}
        url = reverse("reservation-dates-detail", args=[self.reservation.id])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)