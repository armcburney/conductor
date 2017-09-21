class EventAction < ApplicationRecord
  belongs_to :event_receiver
  has_one :job_type
end
