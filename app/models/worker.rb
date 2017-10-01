# frozen_string_literal: true

class Worker < ApplicationRecord
  belongs_to :user
  has_many :jobs

  def self.jobs_length
    jobs.length
  end
end
