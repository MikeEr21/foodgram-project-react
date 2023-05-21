import { Title, Pagination, Container, Main, SubscriptionList  } from '../../components'
import { useSubscriptions } from '../../utils'
import api from '../../api'
import { useEffect } from 'react'
import MetaTags from 'react-meta-tags'

const SubscriptionsPage = () => {
  const {
    subscriptions,
    setSubscriptions,
    subscriptionsCount,
    setSubscriptionsCount,
    removeSubscription,
    subscriptionsPage,
    setSubscriptionsPage
  } = useSubscriptions()

  const getSubscriptions = ({ page }) => {
    api
      .getSubscriptions({ page })
      .then(res => {
        setSubscriptions(res.results)
        setSubscriptionsCount(res.count)
      })
  }

  useEffect(_ => {
    getSubscriptions({ page: subscriptionsPage })
  }, [subscriptionsPage])
const subscribeToUser = (userId) => {
    api.subscribe(userId)
      .then(response => {
        // handle successful case
        getSubscriptions({ page: subscriptionsPage })  // fetch updated subscriptions
      })
      .catch(error => {
        // Handle API errors
        if (error.response) {
          alert(error.response.data.detail);
        } else if (error.request) {
          alert('There was a problem with the request. Please try again.')
        } else {
          alert('There was an error. Please try again.');
        }
      });
  };

  return <Main>
    <Container>
      <MetaTags>
        <title>Мои подписки</title>
        <meta name="description" content="Продуктовый помощник - Мои подписки" />
        <meta property="og:title" content="Мои подписки" />
      </MetaTags>
      <Title
        title='Мои подписки'
      />
      <SubscriptionList
        subscriptions={subscriptions}
        removeSubscription={removeSubscription}
      />
      <Pagination
        count={subscriptionsCount}
        limit={6}
        onPageChange={page => {
          setSubscriptionsPage(page)
        }}
      />
    </Container>
  </Main>
}

export default SubscriptionsPage